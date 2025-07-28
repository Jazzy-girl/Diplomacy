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

from api.models import *
from adjudicator.adjudication import resolve_moves, resolve_retreats, next_turn, resolve_adjustments
from api.tasks import adjudicate_game
from datetime import timedelta
from zoneinfo import ZoneInfo

from tests.tests import orders_to_json

TEMPLATE_SETUP = 'tests/json/templates.json'
VANILLA_UNIT_SETUP = 'tests/json/vanilla_setup.json'
UPDATE_BULK_ORDER = '/api/update/order/bulk/'

CREATE_MESSAGE = '/api/create/message/'
CREATE_CHAIN = '/api/create/chain/'

COASTS_ABBREV = {coast.name : coast for coast in CoastTemplate.objects.all()}

class CircularMovementTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', TEMPLATE_SETUP)
        call_command('loaddata', VANILLA_UNIT_SETUP)
        cls.user = get_user_model().objects.create_user(username="testuser",password="testpass")
    
    def test_circular_movement(self):
        """
        TURKEY: F Ankara Coast -> Constantinople Coast
                A Constantinople -> Smyrna
                A Smyrna -> Ankara
        """
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        game = Game.objects.create(name="Test Game")

        game.started = True
        game.save(update_fields=['started'])
        game.refresh_from_db()

        orders_dict = {order.origin_territory.territory_template.name : order for order in Order.objects.filter(game=game,turn=game.current_turn)}
        order_ank = orders_dict["Ank"]
        order_con = orders_dict["Con"]
        order_smy = orders_dict["Smy"]


        orders = [order_ank, order_con, order_smy]

        commands = [
            "F Ank/c - Con/c",
            "A Con - Smy",
            "A Smy - Ank"
        ]

        data = orders_to_json(instance=game,commands=commands)
        
        response = self.client.patch(UPDATE_BULK_ORDER, data, format="json")
        self.assertEqual(response.status_code, 200)

        resolve_moves(game)

        for order in orders:
            order.refresh_from_db()
            self.assertEqual(order.result, Order.OrderResult.SUCCEEDS)