from django.test import TestCase
from django.core.management import call_command
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch, mock_open
import json
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Game, Territory, Unit, Order, Sandbox, Country, CoastTemplate, TerritoryTemplate
from adjudicator.adjudication import resolve_moves

class GameInitializationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'fixtures/initial_templates.json')

    def test_territories_orders_coutnries_units_created(self,):
        game = Game.objects.create(name="Test Game")
        territories = Territory.objects.all()
        units = Unit.objects.filter(game=game)
        orders = Order.objects.filter(game=game)
        countries = Country.objects.filter(game=game)
        self.assertEqual(countries.count(), 7)
        self.assertEqual(territories.count(), 75)
        self.assertEqual(units.count(), 22)
        self.assertEqual(orders.count(), 22)

class AdjudicationTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'fixtures/initial_templates.json')
        cls.user = get_user_model().objects.create_user(username="testuser",password="testpass")
    
    def test_resolve_moves(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        game = Game.objects.create(name="Test Game")
        bla = Territory.objects.get(game=game,territory_template=TerritoryTemplate.objects.get(name="BLA"))
        ank = Territory.objects.get(game=game,territory_template=TerritoryTemplate.objects.get(name="Ank"))
        ank_coast = CoastTemplate.objects.get(name="Ank")
        sev = Territory.objects.get(game=game,territory_template=TerritoryTemplate.objects.get(name="Sev"))
        sev_coast = CoastTemplate.objects.get(name="Sev")
        order_ank = Order.objects.get(game=game,origin_territory=ank,origin_coast=ank_coast)
        order_sev = Order.objects.get(game=game,origin_territory=sev,origin_coast=sev_coast)


        url = '/api/update/order/bulk/'
        payload = [
            {
                "id": order_ank.pk,
                "target_territory": bla.pk,
                "move_type": "M"
            },
            {
                "id": order_sev.pk,
                "target_territory": bla.pk,
                "move_type": "M"
            }
        ]

        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, 200)

        resolve_moves(game)

        # for order in Order.objects.filter(game=game):
        #     print(order)
        
        order_ank.refresh_from_db()
        order_sev.refresh_from_db()
        self.assertEqual(order_ank.target_territory, bla)
        self.assertEqual(order_ank.move_type, "M")
        self.assertEqual(order_ank.result, 'FAILS')
        self.assertEqual(order_sev.target_territory, bla)
        self.assertEqual(order_sev.move_type, "M")
        self.assertEqual(order_sev.result, "FAILS")

class BulkUpdateOrdersTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', 'fixtures/initial_templates.json')
        cls.user = get_user_model().objects.create_user(username="testuser",password="testpass")
    
    def test_bulk_patch_orders(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        game = Game.objects.create(name="Test Game 2")

        smyTemp = TerritoryTemplate.objects.get(name="Smy")
        syrTemp = TerritoryTemplate.objects.get(name="Syr")
        ankTemp = TerritoryTemplate.objects.get(name="Ank")
        armTemp = TerritoryTemplate.objects.get(name="Arm")

        smy = Territory.objects.get(game=game,territory_template=smyTemp)
        syr = Territory.objects.get(game=game,territory_template=syrTemp)
        ank = Territory.objects.get(game=game,territory_template=ankTemp)
        ank_coast = CoastTemplate.objects.get(name="Ank")
        arm = Territory.objects.get(game=game,territory_template=armTemp)

        order1 = Order.objects.get(game=game, origin_territory=smy)
        order2 = Order.objects.get(game=game, origin_territory=ank, origin_coast=ank_coast)

        url = '/api/update/order/bulk/'
        payload = [
            {
                "id": order1.id,
                "target_territory": syr.id,
                "move_type": "M"
            },
            {
                "id": order2.id,
                "target_territory": arm.id,
                "move_type": "M"
            }
        ]

        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, 200)

        order1.refresh_from_db()
        order2.refresh_from_db()
        self.assertEqual(order1.target_territory, syr)
        self.assertEqual(order1.move_type, "M")
        self.assertEqual(order2.target_territory, arm)
        self.assertEqual(order2.move_type, "M")