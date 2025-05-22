from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Game, Territory, Unit, Order, MoveTypes
import json

TERRITORIES_FILE = '/home/rywilson/DipProject/Diplomacy/frontend/src/assets/territories.json'
UNITS_FILE = '/home/rywilson/DipProject/Diplomacy/frontend/src/assets/countrySetup.json'
@receiver(post_save, sender=Game)
def create_territories_and_units_on_game_save(sender, instance, created, **kwargs):
    print("signal triggered!") #Debug
    if created:
        # First make the Territories
        with open(TERRITORIES_FILE, 'r') as fTerrs:
            data = json.load(fTerrs)
            for name, territory in data.items():
                sc_exists = territory["sc"]
                Territory.objects.create(game=instance, name=name, sc_exists=sc_exists)
        # Then make the Units
        with open(UNITS_FILE, 'r') as fUnits:
            data = json.load(fUnits)
            for country, territories in data.items():
                for territory, type in territories.items():
                    unit = Unit.objects.create(game=instance, location=territory, type=type, owner=country[0])
                    Order.objects.create(game=instance,unit=unit,
                                         country=country[0],
                                         origin_territory=territory,
                                         move_type=MoveTypes.HOLD,
                                         year=1901, season='spring')