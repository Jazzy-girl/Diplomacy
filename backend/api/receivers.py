from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Game, Territory, Unit, Order, Sandbox
from django.conf import settings
import os

import json

TERRITORIES_FILE = os.path.join(settings.BASE_DIR.parent, 'frontend', 'src', 'assets', 'territories.json')
UNITS_FILE = os.path.join(settings.BASE_DIR.parent, 'frontend', 'src', 'assets', 'countrySetup.json')

def create_territories_units_orders_on_game_or_sandbox_save(sender, instance, created, **kwargs):
    print("signal triggered!") #Debug
    if created:
        # First make the Territories
        with open(TERRITORIES_FILE, 'r') as fTerrs:
            data = json.load(fTerrs)
            for name, territory in data.items():
                sc_exists = territory["sc"]
                # add check for coasts
                if isinstance(instance, Game):
                    Territory.objects.create(game=instance, name=name, sc_exists=sc_exists)
                else:
                    Territory.objects.create(sandbox=instance, name=name, sc_exists=sc_exists)
        # Then make the Units
        with open(UNITS_FILE, 'r') as fUnits:
            data = json.load(fUnits)
            for country, territories in data.items():
                for territory, type in territories.items():
                    if isinstance(instance, Game):
                        unit = Unit.objects.create(game=instance, territory=territory, type=type, owner=country[0])
                        Order.objects.create(game=instance,unit=unit,
                                            country=country[0],
                                            origin_territory=territory,
                                            move_type=Order.MoveTypes.HOLD,
                                            turn=1)
                    else:
                        unit = Unit.objects.create(sandbox=instance, territory=territory, type=type, owner=country[0])
                        Order.objects.create(sandbox=instance,unit=unit,
                                            country=country[0],
                                            origin_territory=territory,
                                            move_type=Order.MoveTypes.HOLD,
                                            turn=1)   
post_save.connect(create_territories_units_orders_on_game_or_sandbox_save, sender=Game)
post_save.connect(create_territories_units_orders_on_game_or_sandbox_save, sender=Sandbox)