from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Game, Territory, Unit, Order, Sandbox, TerritoryTemplate, CountryTemplate, Country, InitialUnitSetup, TimeZone
from django.conf import settings
import os
from datetime import timedelta, datetime
from django.utils import timezone
import json
from collections import defaultdict
from zoneinfo import ZoneInfo
from django.utils.timezone import make_aware

def create_territories_units_orders_on_game_or_sandbox_save(sender, instance, created, **kwargs):
    # print("signal triggered!") #Debug
    isGame = isinstance(instance, Game)
    if created:
        """
        Makes:
            - Country for each CountryTemplate
            - Territory for each TerritoryTemplate
            - Unit for each InitialUnitSetup
            - Order for each InitialUnitSetup
        """
        if isGame: # set adjudication
            data = instance.settings.get('adjudication')
            unit = data.get('first_unit')
            start_hour = data.get('start')
            amount = data.get('first_turn')
            zone = ZoneInfo(data.get('timezone'))
            if unit == Game.AdjudicationLength.DAYS:
                delta = timedelta(days=amount)
            elif unit == Game.AdjudicationLength.HOURS:
                delta = timedelta(hours=amount)
            elif unit == Game.AdjudicationLength.MINUTES:
                delta = timedelta(minutes=amount)
            else:
                raise ValueError(f"Incorrect unit: {unit}")
            
            # so far delta doesn't take into account starting at the actual start_time
            """
            Goal: Make the next_adjudication be at least the <delta> amount past the current time while
                  also starting at the start_time. 
            Method: Check the current time + delta and compare to start time on the same day; if less, put next_adjudication at start time on that day;
                    elif more, put next_adjudication at start time on the next day.
            """

            new_time = datetime.now(zone) + delta
            # check if <= or > start time on that day
            month = new_time.month
            year = new_time.year
            day = new_time.day
            if new_time.hour > start_hour: # set next_adjudication to tomorrow
                day += 1
            date = make_aware(datetime(year=year,month=month,day=day,hour=start_hour), timezone=zone)
            instance.next_adjudication = date
            instance.save(update_fields=['next_adjudication'])

        country_templates = CountryTemplate.objects.all()
        countries = {}
        countries[None] = None
        country_scs = defaultdict(int)
        for template in country_templates:
            country = Country.objects.create(country_template=template)
            if isinstance(instance, Game):
                country.game = instance
            else:
                country.sandbox = instance
            country.save()
            countries[country.country_template] = country

        territory_templates = TerritoryTemplate.objects.all()
        # print(f"Loaded {TerritoryTemplate.objects.count()} templates")
        territories = {}
        for template in territory_templates:
            # country = countries[template.country_template]
            territory = Territory.objects.create(territory_template=template)
            if isinstance(instance, Game):
                territory.game = instance
            else:
                territory.sandbox = instance
            territory.save()
            territories[template] = territory
            # if template.sc_exists and template.country_template != None:
            #     country_scs[template.country_template] += 1
        
        setups = InitialUnitSetup.objects.all()
        for setup in setups:
            territory = territories[setup.territory_template]
            country = countries[setup.country_template]
            coast = setup.coast_template
            unit_type = setup.unit_type
            unit = Unit.objects.create(territory=territory, type=unit_type,
                                        country=country, coast=coast)
            order = Order.objects.create(unit=unit,country=country,origin_territory=territory,
                                        origin_coast=coast,move_type=Order.MoveTypes.HOLD, turn=instance.current_turn)
            if isinstance(instance, Game):
                unit.game = instance
                order.game = instance
            else:
                unit.sandbox = instance
                order.sandbox = instance
            unit.save()
            order.save()
            unit.territory.country = unit.country
            unit.territory.save()
            if unit.territory.territory_template.sc_exists:
                country_scs[unit.country.pk] += 1
        for template, country in countries.items():
            # print(f"{template} : {country}")
            if template != None:
                # print(f"{country.country_template.full_name} : {country_scs[country.pk]}")
                country.scs = country_scs[country.pk]
                country.save()
post_save.connect(create_territories_units_orders_on_game_or_sandbox_save, sender=Game)
post_save.connect(create_territories_units_orders_on_game_or_sandbox_save, sender=Sandbox)