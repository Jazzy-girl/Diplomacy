from pydip.player.unit import (
    Unit as PyDipUnit,
    UnitTypes as PyDipUnitTypes
)

from pydip.player.command.command import (
    ConvoyMoveCommand,
    ConvoyTransportCommand,
    HoldCommand,
    MoveCommand,
    SupportCommand
)

import json
from pydip.player.command.retreat_command import RetreatDisbandCommand, RetreatMoveCommand

from pydip.player import Player

from pydip.map.predefined import vanilla_dip

from api.models import (
    Game, Sandbox, Country, Order, Territory, TerritoryTemplate, 
    CoastTemplate, CountryTemplate, UnitType, UnitRetreatOption, AdjustmentCache,
    CountrySCCountSnapshot, TerritoryCountrySnapshot, UnitLocationSnapshot
    )

from api.models import Unit as DjangoUnit

from collections import defaultdict

from pydip.turn.resolve import resolve_turn
"""
THE ADJUDICATOR!

    - Loads the vanilla map (for now; later will introduce variants)
    - Loads units and orders into place
"""
def adjudicate(instance: Game | Sandbox):
    """
    Takes in an instance of either a Game or Sandbox and calls
    the necessary functions.
    """
    SPRING = 0
    FALL = 1
    WINTER = 2
    season = instance.current_turn % 3
    if season == SPRING or FALL:
        if instance.retreat_required:
            return resolve_retreats(instance)
        else:
            return resolve_moves(instance)
    else:
        return resolve_adjustments(instance)

def resolve_moves(instance: Game):
    game_map = vanilla_dip.generate_map()
    players = {}
    if isinstance(instance, Game):
        units = DjangoUnit.objects.filter(game=instance)
        orders = { order.origin_coast.full_name if order.origin_coast else order.origin_territory.territory_template.full_name : order for order in Order.objects.filter(game=instance, turn=instance.current_turn)}
        territories = {territory.territory_template.full_name : territory for territory in Territory.objects.filter(game=instance)}
    else:
        units = DjangoUnit.objects.filter(sandbox=instance)
        orders = Order.objects.filter(sandbox=instance, turn=instance.current_turn)
        territories = {territory.territory_template.full_name : territory for territory in Territory.objects.filter(sandbox=instance)}
    coasts = {coast.full_name : coast for coast in CoastTemplate.objects.all()}
    player_units = defaultdict(list)

    game_units = {}
    
    commands = []

    for unit in units:
        if unit.coast:
            position = unit.coast.full_name
        else:
            position = unit.territory.territory_template.full_name
        # print(position)
        unit_type = PyDipUnitTypes.TROOP if unit.type == 'A' else PyDipUnitTypes.FLEET
        game_unit = PyDipUnit(unit_type,position)
        game_units[unit.territory.territory_template.full_name] = game_unit
        player_name = unit.country.country_template.full_name
        player_units[player_name].append(game_unit)

    for name in player_units.keys():
        player = Player(name, game_map, starting_configuration=[], starting_units=player_units[name])
        players[name] = player
        # print(player)

    for order in orders.values():
        player = players[order.country.country_template.full_name]
        if order.origin_coast:
            unit = player.find_unit(order.origin_coast.full_name)
        else:
            unit = player.find_unit(order.origin_territory.territory_template.full_name)
        
        if order.target_territory:
            if order.target_coast:
                destination = order.target_coast.full_name
            else:
                destination = order.target_territory.territory_template.full_name
        
        match order.move_type:
            case Order.MoveTypes.HOLD:
                cmd = HoldCommand(player, unit)
            case Order.MoveTypes.MOVE:
                cmd = MoveCommand(player, unit, destination)
            case Order.MoveTypes.SUPPORT:
                if order.supported_coast:
                    supported_unit = game_units[order.supported_coast.full_name]
                else:
                    supported_unit = game_units[order.supported_territory.territory_template.full_name]
                cmd = SupportCommand(player,unit,supported_unit,destination)
            case Order.MoveTypes.CONVOY:
                transported_unit = game_units[order.convoyed_territory.territory_template.full_name]
                cmd = ConvoyTransportCommand(player, unit, transported_unit, destination)
            case Order.MoveTypes.MOVE_VIA_CONVOY:
                cmd = ConvoyMoveCommand(player, unit, destination)
        # print(cmd)
        commands.append(cmd)

    order_results = resolve_turn(game_map, commands)
    # print(commands)
    for home_territory, values in order_results.items():
        order = orders[home_territory]
        result = values[0]
        new_location = values[1]
        dislodged = True if values[2] != None else False
        retreat_locations = values[2]
        failure_reason = values[3]

        order.result = 'SUCCEEDS' if result else 'FAILS'
        order.dislodged = dislodged
        if dislodged:
            if len(retreat_locations) > 0:
                order.retreat_required = True 
            else:
                order.retreat_required = False
                order.retreat_result = 'D'
                order.unit.disbanded = True
            
        if(order.retreat_required):
            if not instance.retreat_required:
                instance.retreat_required = True
                instance.save()
            for retreat_location in retreat_locations:
                coast = None
                if 'Coast' in retreat_location:
                    coast = coasts[retreat_location]
                territory = territories[retreat_location]
                # print(f"RETREAT TERRITORY: {retreat_location}")
                if isinstance(instance, Game):
                    retreat_option = UnitRetreatOption.objects.create(order=order,territory=territory,coast=coast,game=instance,turn=instance.current_turn)
                else:
                    retreat_option = UnitRetreatOption.objects.create(order=order,territory=territory,coast=coast,sandbox=instance,turn=instance.current_turn)
        order.save()
        # print(order)
    if(instance.retreat_required):
        return -1
    else:
        return next_turn(instance)

def resolve_retreats(instance: Game):
    """
    Resolves retreats.
    """
    if isinstance(instance, Game):
        retreat_orders = Order.objects.filter(game=instance,turn=instance.current_turn,retreat_required=True)
    else:
        retreat_orders = Order.objects.filter(sandbox=instance,turn=instance.current_turn,retreat_required=True)
    for order in retreat_orders:
        other_orders = list(filter(lambda c: c!=order, retreat_orders))
        if all(order.retreat_territory != other_order.retreat_territory for other_order in other_orders):
            order.retreat_result = 'R'
        else:
            order.retreat_result = 'D'
            order.unit.disbanded = True
        order.save()
    instance.retreat_required = False
    instance.save()
    # call a new turn!
    return next_turn(instance)

def resolve_adjustments(instance: Game):
    """
    Resolves Winter builds and disbands.
    """
    # Take in build & disband orders. Create and disband units
    isGame = True if isinstance(instance, Game) else False
    if isGame:
        units = DjangoUnit.objects.filter(game=instance,disbanded=False,country__needed_disbands__gt=0)
        orders = Order.objects.filter(game=instance,turn=instance.current_turn) # ADD: constraint for needs disband or available builds
        countries = Country.objects.filter(game=instance)
    else:
        units = DjangoUnit.objects.filter(sandbox=instance,disbanded=False,country__needed_disbands__gt=0)
        orders = Order.objects.filter(sandbox=instance,turn=instance.current_turn)
        countries = Country.objects.filter(sandbox=instance)

    build_orders = defaultdict(list)
    disband_orders = defaultdict(list)
    for order in orders:
        country = order.country.country_template.name
        if order.adjustment_type == 'D':
            disband_orders[country].append(order)
        elif order.adjustment_type == 'B':
            build_orders[country].append(order)
        else:
            raise ValueError(f"Order's adjustment type is incorrect: {order.adjustment_type}")
    
    for country in countries:
        disbands = list()
        
        builds = list()
        if country.needed_disbands > 0:
            """
            If disbands are needed:
                - If the amount of disband orders <= needed disbands: Iterate through the disband orders
                - If the amount of disband orders < needed disbands: After iterating, perform other needed disbands alphabetically
                - If the amount of disband orders > needed disbands: Order alphabetically, iterate through up until reaching the needed amount of disbands. (Fail the others)
            """
            needed = country.needed_disbands
            disbands = disband_orders[country.country_template.name]
            disbands.sort(key=lambda o: o.unit.coast.full_name if o.unit.coast else o.unit.territory.territory_template.full_name)
            disband_count = 0
            for disband in disbands: # disband = Order
                if(disband_count < needed): # Its chill
                    disband.unit.disbanded = True
                    disband.result = Order.OrderResult.SUCCEEDS
                    disband.unit.save()
                    disband.save()
                    disband_count += 1
                else: # it's NOT chill
                    disband.result = Order.OrderResult.FAILS
                    disband.save()
                    # TO ADD: the failure reason...
            if len(disbands) < needed: # Do the rest!
                to_disband = [unit for unit in units if (unit.disbanded == False and unit.country == country)]
                to_disband.sort(key=lambda u: u.coast.full_name if u.coast else u.territory.territory_template.full_name)
                for disbanded_unit in to_disband[0:(needed-len(disbands)+1)]:
                    Order.objects.create(game=instance,unit=disbanded_unit, country=country,
                                            turn=instance.current_turn,adjustment_type=Order.AdjustmentTypes.DISBAND,
                                            result=Order.OrderResult.SUCCEEDS)
                    disbanded_unit.disbanded = True
                    disbanded_unit.save()

        if country.available_builds > 0:
            """
            Order builds alphabetically
            If more builds than available: stop and FAIL the rest
            if fewer builds than available: continue as normal
            """
            builds = build_orders[country.country_template.name]
            allowed = country.available_builds
            built = 0
            builds.sort(key=lambda o: o.unit.coast.full_name if o.unit.coast else o.unit.territory.territory_template.full_name)
            for build in builds:
                if(built < allowed):
                    territory = build.build_territory
                    coast = build.build_coast
                    unit_type = build.build_type
                    country = build.country
                    if isGame:
                        unit = DjangoUnit.objects.create(game=instance,territory=territory,coast=coast,type=unit_type,country=country)
                    else:
                        unit = DjangoUnit.objects.create(sandbox=instance,territory=territory,coast=coast,type=unit_type,country=country)
                    build.unit = unit
                    build.result = Order.OrderResult.SUCCEEDS
                    built += 1
                else:
                    build.result = Order.OrderResult.FAILS
                build.save()
    return next_turn(instance)



def next_turn(instance: Game):
    SPRING = 0
    FALL = 1
    WINTER = 2
    turn = instance.current_turn
    new_turn = turn + 1
    season = turn % 3

    isGame = True if isinstance(instance, Game) else False

    def _get_new_locations(order=Order):
        """
        Takes in an order, returns the updated origin territory and coast of a unit / new order
        """
        if order.retreat_result == 'R':
            origin_territory, origin_coast = order.retreat_territory, order.retreat_coast
        elif (order.move_type == 'M' or order.move_type == 'V') and order.result == 'SUCCEEDS':
            origin_territory, origin_coast = order.target_territory, order.target_coast
        else:
            origin_territory, origin_coast = order.origin_territory, order.origin_coast
        return origin_territory, origin_coast
    
    if season == SPRING:
        # Based on each order: make new hold orders for each non disbanded order, and update unit locations.
        if isinstance(instance, Game):
            orders = Order.objects.filter(game=instance,turn=instance.current_turn,unit__disbanded=False) # Excludes Disbanded orders
        else:
            orders = Order.objects.filter(sandbox=instance,turn=instance.current_turn,unit__disbanded=False) # Excludes Disbanded orders
        for order in orders:
            origin_territory, origin_coast = _get_new_locations(order)
            # print(f"TESTING: {origin_territory} {origin_coast}")
            country = order.country
            unit = order.unit
            unit.territory = origin_territory
            unit.coast = origin_coast
            unit.save()
            if isinstance(instance, Game):
                new_order = Order.objects.create(game=instance,turn=new_turn,unit=unit,country=country,origin_territory=origin_territory,origin_coast=origin_coast,move_type='H')
            else:
                new_order = Order.objects.create(sandbox=instance,turn=new_turn,unit=unit,country=country,origin_territory=origin_territory,origin_coast=origin_coast,move_type='H')
    elif season == FALL:
        """
        Update unit locations, owned territories, sc counts, make available build and disband cache
        Make new entries into the AdjustmentCache if necessary
        Make new entries into the TerritoryCountrySnapshot & CountrySCCountSnapshot tables
        """
        if isinstance(instance, Game):
            units = DjangoUnit.objects.filter(game=instance,disbanded=False)
            countries = Country.objects.filter(game=instance)
            orders = Order.objects.filter(game=instance,turn=instance.current_turn,unit__disbanded=False) # Excludes Disbands
        else:
            units = DjangoUnit.objects.filter(sandbox=instance,disbanded=False)
            countries = Country.objects.filter(sandbox=instance)
            orders = Order.objects.filter(sandbox=instance,turn=instance.current_turn,unit__disbanded=False) # Excludes Disbands
        unit_count = defaultdict(int)
        for order in orders:
            unit = order.unit
            unit.territory, unit.coast = _get_new_locations(order)
            unit.territory.country = unit.country
            unit.territory.save()
            unit.save()
            unit_count[order.country.pk] += 1
            # Make entries into the TerritoryCountrySnapshot table!
            if isGame:
                TerritoryCountrySnapshot.objects.create(game=instance,territory=unit.territory,country=unit.country,turn=instance.current_turn)
            else:
                TerritoryCountrySnapshot.objects.create(sandbox=instance,territory=unit.territory,country=unit.country,turn=instance.current_turn)
        if isinstance(instance, Game):
            scs = Territory.objects.filter(game=instance,territory_template__sc_exists=True)
            occupied_territories = {unit.territory for unit in DjangoUnit.objects.filter(game=instance,disbanded=False)}
        else:
            scs = Territory.objects.filter(sandbox=instance,territory_template__sc_exists=True)
            occupied_territories = {unit.territory for unit in DjangoUnit.objects.filter(sandbox=instance,disbanded=False)}
        coasts = CoastTemplate.objects.all()
        sc_count = defaultdict(int)
        
        for sc in scs:
            if sc.country:
                sc_count[sc.country.pk] += 1
        disband_cache = defaultdict(list) # JSON
        build_cache = defaultdict(list) # JSON
        for country in countries:
            # print(f"{country.country_template.full_name} : SC COUNT = {sc_count[country.pk]}; UNIT COUNT = {unit_count[country.pk]}")
            country.scs = sc_count[country.pk]
            # Make entries into the CountrySCCount table
            if isGame:
                CountrySCCountSnapshot.objects.create(game=instance, country=country, scs=sc_count[country.pk], turn=instance.current_turn)
            else:
                CountrySCCountSnapshot.objects.create(sandbox=instance, country=country, scs=sc_count[country.pk], turn=instance.current_turn)
            difference = sc_count[country.pk] - unit_count[country.pk]
            if difference < 0:
                country.needed_disbands = (difference * -1)
                # make disbands JSON list
                # Format: <Country> : [<Unit>, <Unit>, ...]
                disband_cache[country.pk] = [order.unit.pk for order in orders if order.unit.country==country]
            elif difference > 0:
                # make builds JSON list of unoccupied home centers
                base_territories = [
                    sc for sc in scs
                    if sc.country==country and sc.territory_template.home_center==True
                    and sc.territory_template.country_template==country.country_template
                    and sc not in occupied_territories
                ]
                
                build_cache[country.pk] = [sc.pk for sc in base_territories]

                valid_terr_templates = {sc.territory_template for sc in base_territories}
                build_cache[country.pk].extend([coast.pk for coast in coasts if coast.territory_template in valid_terr_templates])
                country.available_builds = min(difference, len(build_cache[country.pk]))
            country.save()    
        # CHECK: Are there 0 needed disbands & 0 available builds? if so skip RIGHT through winter to Spring!!!
        if not disband_cache and not build_cache: # Empty
            # skip right through winter to spring!
            instance.current_turn += 1
        else: # they aint empty
            for unit in units:
                # This will make a UnitLocationSnapshot for each unit in the Winter turn excepting the newly built units.
                if isGame:
                    UnitLocationSnapshot.objects.create(game=instance,unit=unit,territory=unit.territory,coast=unit.coast,turn=new_turn)
                else:
                    UnitLocationSnapshot.objects.create(sandbox=instance,unit=unit,territory=unit.territory,coast=unit.coast,turn=new_turn)
            if isinstance(instance, Game):
                adjustmentCache = AdjustmentCache.objects.create(game=instance,turn=new_turn,build_cache=build_cache,disband_cache=disband_cache)
            elif isinstance(instance, Sandbox):
                adjustmentCache = AdjustmentCache.objects.create(sandbox=instance,turn=new_turn,build_cache=build_cache,disband_cache=disband_cache)
            # winter has begun
    elif season == WINTER:
        # Make new default hold orders for each living unit
        if isGame:
            units = DjangoUnit.objects.filter(game=instance,disbanded=False)
        else:
            units = DjangoUnit.objects.filter(sandbox=instance,disbanded=False)
        for unit in units:
            if isGame:
                order = Order.objects.create(game=instance,country=unit.country,turn=new_turn,unit=unit,origin_territory=unit.territory,origin_coast=unit.coast,move_type=Order.MoveTypes.HOLD)
            else:
                order = Order.objects.create(game=instance,country=unit.country,turn=new_turn,unit=unit,origin_territory=unit.territory,origin_coast=unit.coast,move_type=Order.MoveTypes.HOLD)
    instance.current_turn += 1
    instance.save()
    return instance.current_turn