from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Game, Territory, Unit, Order, Sandbox, TerritoryTemplate, CountryTemplate, Country
from django.conf import settings
import os

import json

TERRITORIES_FILE = os.path.join(settings.BASE_DIR.parent, 'frontend', 'src', 'assets', 'territories.json')
UNITS_FILE = os.path.join(settings.BASE_DIR.parent, 'frontend', 'src', 'assets', 'countrySetup.json')

def create_territories_units_orders_on_game_or_sandbox_save(sender, instance, created, **kwargs):
    print("signal triggered!") #Debug
    if created:
        """
        Makes:
            - Country for each CountryTemplate
            - Territory for each TerritoryTemplate
            - Unit for each unit in TerritoryTemplate
            - Order for each Unit
        """
        # First make the Territories
        # with open(TERRITORIES_FILE, 'r') as fTerrs:
        #     data = json.load(fTerrs)
        #     for name, territory in data.items():
        #         sc_exists = territory["sc"]
        #         # add check for coasts
        #         if isinstance(instance, Game):
        #             Territory.objects.create(game=instance, name=name, sc_exists=sc_exists)
        #         else:
        #             Territory.objects.create(sandbox=instance, name=name, sc_exists=sc_exists)

        country_templates = CountryTemplate.objects.all()
        countries = {}
        countries[None] = None
        for template in country_templates:
            if isinstance(instance, Game):
                country = Country.objects.create(game=instance, country_template=template, scs=template.scs)
            else:
                country = Country.objects.create(sandbox=instance, country_template=template, scs=template.scs)
            countries[country.country_template] = country

        territory_templates = TerritoryTemplate.objects.all()
        for template in territory_templates:
            country = countries[template.country_template]
            if isinstance(instance, Game):
                territory = Territory.objects.create(game=instance,territory_template=template,country=country)
                # if template.unit_type:
                #     unit = Unit.objects.create(game=instance, territory=territory, type=template.unit_type, country=country, coast=template.coast_template)
                #     order = Order.objects.create(game=instance,unit=unit,country=country,origin_territory=territory,
                #                                  origin_coast=template.unit_coast,move_type=Order.MoveTypes.HOLD,turn=1)
            else:
                territory = Territory.objects.create(sandbox=instance,territory_template=template,country=country)

        # # Then make the Units
        # with open(UNITS_FILE, 'r') as fUnits:
        #     data = json.load(fUnits)
        #     for country, territories in data.items():
        #         for territory, type in territories.items():
        #             if isinstance(instance, Game): # Game
        #                 terr = Territory.objects.filter(name=territory, game=instance).all()
        #                 # ctry = ...
        #                 unit = Unit.objects.create(game=instance, territory=terr, type=type, owner=country[0])
        #                 Order.objects.create(game=instance,unit=unit,
        #                                     country=country[0],
        #                                     origin_territory=territory,
        #                                     move_type=Order.MoveTypes.HOLD,
        #                                     turn=1)
        #             else: # Sandbox
        #                 terr = Territory.objects.filter(name=territory, sandbox=instance).all()
        #                 unit = Unit.objects.create(sandbox=instance, territory=terr, type=type, owner=country[0])
        #                 Order.objects.create(sandbox=instance,unit=unit,
        #                                     country=country[0],
        #                                     origin_territory=territory,
        #                                     move_type=Order.MoveTypes.HOLD,
        #                                     turn=1)   
post_save.connect(create_territories_units_orders_on_game_or_sandbox_save, sender=Game)
post_save.connect(create_territories_units_orders_on_game_or_sandbox_save, sender=Sandbox)