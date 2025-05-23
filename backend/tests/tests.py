from django.test import TestCase
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from unittest.mock import patch, mock_open
import json

from api.models import Game, Territory, Unit

class GameInitializationTest(TestCase):
    @patch("api.receivers.open", new_callable=mock_open)
    def test_territories_and_units_created(self, mock_open_fn):
        #Mock Data
        territory_json = json.dumps({
            "Ank": {"sc": True},
            "Arm": {"sc": False},
            "Smy": {"sc": True}
        })
        units_json = json.dumps({
            "Turkey":{
                "Ank": "F"
            },
        })
        mock_territory = mock_open(read_data=territory_json).return_value
        mock_units = mock_open(read_data=units_json).return_value
        mock_open_fn.side_effect = [mock_territory, mock_units]
        game = Game.objects.create(name="Test Game")
        territories = Territory.objects.filter(game=game)
        units = Unit.objects.filter(game=game)
        self.assertEqual(territories.count(), 3)
        self.assertEqual(units.count(), 1)