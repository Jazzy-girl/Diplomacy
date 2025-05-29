from django.test import TestCase
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch, mock_open
import json
from rest_framework.test import APIClient

from api.models import Game, Territory, Unit, Order, Sandbox

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

class BulkUpdateOrdersTest(TestCase):
    @patch("api.receivers.open", new_callable=mock_open)
    def setUp(self, mock_open_fn):
        #Mock Data
        territory_json = json.dumps({
            "Ank": {"sc": True},
            "Arm": {"sc": False},
            "Sev": {"sc": True},
            "Syr": {"sc": False},
            "Mos": {"sc": False}
        })
        units_json = json.dumps({
            "Turkey":{
                "Ank": "F",
                "Sev": "F"
            },
        })
        mock_territory = mock_open(read_data=territory_json).return_value
        mock_units = mock_open(read_data=units_json).return_value
        mock_open_fn.side_effect = [mock_territory, mock_units]
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(username="tester",email="test@example.com", password="123456789!")
        self.client.force_authenticate(user=self.user)
        self.game = Game.objects.create(name="Test Game")

        self.unit1 = Unit.objects.filter(game=self.game, territory="Ank").first()
        self.unit2 = Unit.objects.filter(game=self.game, territory="Sev").first()
        self.order1 = self.unit1.orders_as_unit.first()
        self.order2 = self.unit2.orders_as_unit.first()

    def test_bulk_patch_orders(self):
        url = '/api/update/order/bulk/'
        payload = [
            {
                "id": self.order1.id,
                "target_territory": "Syr",
                "move_type": "M"
            },
            {
                "id": self.order2.id,
                "target_territory": "Mos",
                "move_type": "M"
            }
        ]

        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, 200)

        self.order1.refresh_from_db()
        self.order2.refresh_from_db()

        self.assertEqual(self.order1.target_territory, "Syr")
        self.assertEqual(self.order1.move_type, "M")
        self.assertEqual(self.order2.target_territory, "Mos")
        self.assertEqual(self.order2.move_type, "M")