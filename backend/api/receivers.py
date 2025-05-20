from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Game, Territory, Unit
import json

@receiver(post_save, sender=Game)
def create_territories_and_units_on_game_save(sender, instance, created, **kwargs):
    if created:
        # First make the Territories
        with open('/home/rywilson/DipProject/Diplomacy/frontend/src/assets/countrySetup.json', 'r') as fTerrs:
            data = json.load(fTerrs)
            for name, territory in data.items():
                sc_exists = territory["sc"]
                Territory.objects.create(game=instance, name=name, sc_exists=sc_exists)
        # Then make the Units