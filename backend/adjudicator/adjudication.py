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

from api.models import Game, Sandbox, Country, Order, Unit, Territory, TerritoryTemplate, CoastTemplate, CountryTemplate, UnitType
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
def resolve(instance=Game):
    # instance is either a Game or Sandbox
    # if isinstance(instance, Game):
    # 1: Load Map
    game_map = vanilla_dip.generate_map()

    # game_map = vanilla_map.supply_map.game_map
    print(game_map)

    # 2: Load Players
    players = {}
    units = Unit.objects.filter(game=instance)
    countries = Country.objects.filter(game=instance)
    territories = Territory.objects.filter(game=instance)
    orders = Order.objects.filter(game=instance, turn=instance.current_turn)
    game_units = {}
    
    """
    NEED:
    - access to player full_name by country id.
    """
    # iterate by country
    # TURN INTO LIST COMPREHENSION LATER like so: starting_config = [dict(territory_name=u.position, unit_type=u.unit_type) for u in units]
    # commands = []

    # for country in countries:
    #     name = CountryTemplate.objects.get(country.country_template).full_name
    #     starting_units = []
    #     for unit in units.filter(country=country):
    #         position = TerritoryTemplate.objects.get(unit.territory.territory_template).full_name
    #         unit_type = PyDipUnitTypes.TROOP if unit.type == 'A' else PyDipUnitTypes.FLEET
    #         game_unit = Unit(unit_type,position)
    #         starting_units.append(game_unit)
    #         game_units[position] = game_unit
    #         # starting_units.append({'territory_name': position, 'unit_type': unit_type})

    #     player = Player(name, game_map, starting_units)
    #     players[name] = player
    #     print(players[name])


    # for order in orders:
    #     player = players[order.country.country_template.full_name]
    #     if order.origin_coast:
    #         unit = player.find_unit(order.origin_coast.full_name)
    #     else:
    #         unit = player.find_unit(order.unit.territory.territory_template.full_name)
        
    #     if order.target_territory:
    #         if order.target_coast:
    #             dest = order.target_coast.full_name
    #         else:
    #             dest = order.target_territory.territory_template.full_name
        
    #     match order.move_type:
    #         case Order.MoveTypes.HOLD:
    #             cmd = HoldCommand(player, unit)
    #         case Order.MoveTypes.MOVE:
    #             cmd = MoveCommand(player, unit, dest)
    #         case Order.MoveTypes.SUPPORT:
    #             supported_unit = 
    #         case Order.MoveTypes.CONVOY:
    #         case Order.MoveTypes.MOVE_VIA_CONVOY:
    #     print(cmd)
    #     commands.append(cmd)
                            



