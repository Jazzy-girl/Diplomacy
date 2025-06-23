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

from pydip.player import Player

from pydip.map.predefined import vanilla_dip

from api.models import Game, Sandbox, Country, Order, Territory, TerritoryTemplate, CoastTemplate, CountryTemplate, UnitType, UnitRetreatOption
from api.models import Unit as DjangoUnit

from collections import defaultdict

from pydip.turn.resolve import resolve_turn
"""
THE ADJUDICATOR!

    - Loads the vanilla map (for now; later will introduce variants)
    - Loads units and orders into place

How to:
Needs
- Player takes a name, the map, and the config of units in form of a dict of (territory_name: <territory name>, unit_type: <unit type; TROOP (0) v FLEET (1)> )
- To get this: 
    - need units: need the full name of the territory template of their territory, 
                  the (potential) full name of their coasttemplate,
                  the full name of the country template of their country
"""
def resolve_moves(instance=Game):
    # instance is either a Game or Sandbox
    # if isinstance(instance, Game):
    # 1: Load Map
    game_map = vanilla_dip.generate_map()

    # 2: Load Players
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
    """
    units plan
    - 
    """
    game_units = {}
    
    """
    NEED:
    - access to player full_name by country id.
    - access to a Unit instance by the territory, options:
        1. make a dict of territory : unit instance pairs
        2. use the order's supported territory ID to find the order that uses that as a home territory... 
                   and then use that order's country.country_template.full_name for the player... and then find_unit...
    """
    # iterate by country
    # TURN INTO LIST COMPREHENSION LATER like so: starting_config = [dict(territory_name=u.position, unit_type=u.unit_type) for u in units]
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
        order.retreat_required = True if dislodged and len(retreat_locations) > 0 else False
        if(order.retreat_required):
            if not instance.retreat_required:
                instance.retreat_required = True
                instance.save()
            if len(retreat_locations) == 0:
                order.retreat_result = 'D'
            else:
                for retreat_location in retreat_locations:
                    coast = None
                    if 'Coast' in retreat_location:
                    #     coast = orders[retreat_location].origin_coast
                        coast = coasts[retreat_location]
                    territory = territories[retreat_location]
                    print(f"RETREAT TERRITORY: {retreat_location}")
                    if isinstance(instance, Game):
                        retreat_option = UnitRetreatOption.objects.create(order=order,territory=territory,coast=coast,game=instance,turn=instance.current_turn)
                    else:
                        retreat_option = UnitRetreatOption.objects.create(order=order,territory=territory,coast=coast,sandbox=instance,turn=instance.current_turn)
        order.save()
        # print(order)
    if(instance.retreat_required):
        # Retreats are required; end;
        pass
    else:
        pass
        # Go to the next turn
        # next_turn(instance)
            # 1 4 7 = Spring
            # 2 5 8 = Fall
            # 3 6 9 = Winter
            # whats the math here?
            # what if we started at 0
            # 0 3 6 = Spring
            # 1 4 7 = Fall
            # 2 5 8 = Winter
            # math here:
            # if divisible by 3, its spring
            # if divisible by 3 with a remainder of 1, its Fall
            # if divisible by 3 with a remainder of 2, its Winter
# def next_turn(instance=Game):
#     turn = instance.current_turn
#     match turn % 3:
#         case 0: # Spring
#             # Based on each order: update Unit location, disband? state; make new hold orders
#             pass
#         case 1: # Fall
#             # Update owned territories / supply centers
#             # Based on each order: update Unit location, disband? state;
#             pass
#         case 2: # Winter
#             # Based on each order: make new units as necessary and disband units as necessary.
#             # Make new default hold orders for each living unit
#             pass
#     instance.current_turn += 1
        



                            



