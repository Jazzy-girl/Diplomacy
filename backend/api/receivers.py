from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Game, Territory, Unit, Order, Sandbox, TerritoryTemplate, CountryTemplate, Country, InitialUnitSetup
from django.conf import settings
import os

import json

def create_territories_units_orders_on_game_or_sandbox_save(sender, instance, created, **kwargs):
    print("signal triggered!") #Debug
    if created:
        """
        Makes:
            - Country for each CountryTemplate
            - Territory for each TerritoryTemplate
            - Unit for each InitialUnitSetup
            - Order for each InitialUnitSetup
        """
        country_templates = CountryTemplate.objects.all()
        countries = {}
        countries[None] = None
        for template in country_templates:
            country = Country.objects.create(country_template=template, scs=template.scs)
            if isinstance(instance, Game):
                country.game = instance
            else:
                country.sandbox = instance
            country.save()
            countries[country.country_template] = country

        territory_templates = TerritoryTemplate.objects.all()
        print(f"Loaded {TerritoryTemplate.objects.count()} templates")
        territories = {}
        for template in territory_templates:
            country = countries[template.country_template]
            territory = Territory.objects.create(territory_template=template,country=country)
            if isinstance(instance, Game):
                territory.game = instance
            else:
                territory.sandbox = instance
            territory.save()
            territories[template] = territory
        
        setups = InitialUnitSetup.objects.all()
        for setup in setups:
            territory = territories[setup.territory_template]
            country = countries[setup.country_template]
            coast = setup.coast_template
            unit_type = setup.unit_type
            unit = Unit.objects.create(territory=territory, type=unit_type,
                                        country=country, coast=coast)
            order = Order.objects.create(unit=unit,country=country,origin_territory=territory,
                                        origin_coast=coast,move_type=Order.MoveTypes.HOLD,turn=1)
            if isinstance(instance, Game):
                unit.game = instance
                order.game = instance
            else:
                unit.sandbox = instance
                order.sandbox = instance
            unit.save()
            order.save()
post_save.connect(create_territories_units_orders_on_game_or_sandbox_save, sender=Game)
post_save.connect(create_territories_units_orders_on_game_or_sandbox_save, sender=Sandbox)