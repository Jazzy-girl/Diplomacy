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

from api.models import Game, Territory, Unit, Order, Sandbox, Country, CoastTemplate, TerritoryTemplate, UnitRetreatOption
from adjudicator.adjudication import resolve_moves, resolve_retreats

TEMPLATE_SETUP = 'tests/json/templates.json'
VANILLA_UNIT_SETUP = 'tests/json/vanilla_setup.json'
UPDATE_BULK_ORDER = '/api/update/order/bulk/'

COASTS_ABBREV = {coast.name : coast for coast in CoastTemplate.objects.all()}
# TERRITORY_TEMPLATES = {}
def orders_to_json(instance=Game,commands=list()):
    """
    Converts a list of orders to json for use with Bulk Update Orders.
    Returns a JSON file.

    :param Game / Sandbox instance:
    :param list commands: format of each order is basic diplomacy; - = Move, H = Hold, S = Support, C = Convoy, V = Move via Convoy; for territories, use three-letter abbrev. for non-specific coasts, use Lon/c; for Retreats, use A Ber R Mun, A Ber D (disbands)
    """
    if isinstance(instance, Game):
        territories = {territory.territory_template.name : territory.pk for territory in Territory.objects.filter(game=instance)}
        orders = {order.origin_coast.pk if order.origin_coast else order.origin_territory.pk : order.pk for order in Order.objects.filter(game=instance,turn=instance.current_turn)}
    else:
        territories = {territory.territory_template.name : territory.pk for territory in Territory.objects.filter(sandbox=instance)}
        orders = {order.origin_coast.pk if order.origin_coast else order.origin_territory.pk : order.pk for order in Order.objects.filter(sandbox=instance,turn=instance.current_turn)}
    
    def get_pk(location=str()):
        """
        takes the territory / coast location

        :return: a tuple of the territory_pk and coast_pk if applicable, otherwise None
        :rtype: (territory_pk, coast_pk)
        """
        if location in territories.keys():
            # is a territory
            return territories[location], None
        else:
            # hopefully is a coast
            if '/c' in location:
                location = location.replace('/c', '')
            if location in COASTS_ABBREV.keys():
                coast = COASTS_ABBREV[location]
                territory = territories[coast.territory_template.name]
                return territory, coast.pk
            else:
                raise ValueError(f"Incorrect Territory Input; must be THREE AND ONLY THREE letters if land/sea, or either Lon/c or Bul/ec if coastal : {location}")
    # parsing the order; <unit type> <territory> <move type> <another order | destination territory>
    data = []
    # print(comma)
    for command in commands:
        pieces = command.split(" ")
        unit_type = pieces[0]
        origin_territory, origin_coast = get_pk(pieces[1])
        if origin_coast is not None:
            id = orders[origin_coast]
        else:
            id = orders[origin_territory]
        target_territory = None
        target_coast = None
        supported_territory = None
        supported_coast = None
        convoyed_territory = None
        retreat_territory = None
        retreat_coast = None
        move_type = pieces[2]
        if move_type == '-':
            move_type = 'M'
            assert len(pieces) == 4 # should be A Bul - Con; 4 long
            target_territory, target_coast = get_pk(pieces[3])
        elif move_type == 'H':
            # nothing really...
            pass
        elif move_type == 'S':
            # A Con S Ank - Smy
            # A Con S Ank H
            assert len(pieces) == 5 or len(pieces) == 6
            supported_territory, supported_coast = get_pk(pieces[3])
            if len(pieces) == 6:
                target_territory, target_coast = get_pk(pieces[5])
            else:
                target_territory, target_coast = supported_territory, supported_coast
        elif move_type == 'C':
            # F BLA C Con - Rom
            convoyed_territory, origin_coast = get_pk(pieces[3])
            assert len(pieces) == 6
            target_territory, target_coast = get_pk(pieces[5])
        elif move_type == 'V':
            assert len(pieces) == 4 # should be A Bul - Con; 4 long
            target_territory, target_coast = get_pk(pieces[3])
        elif move_type == 'R': # Retreat!
            # A Bul R Con; 4 long
            assert len(pieces) == 4
            retreat_territory, retreat_coast = get_pk(pieces[3])
        elif move_type == 'D': # Disband
            # A Bul D
            assert len(pieces) == 3
        else: # Not a move type
            raise ValueError(f"Not a Valid Move Type: {move_type}")

        if move_type == 'R':
            command_data = {
                "id": id,
                "retreat_territory": retreat_territory,
                "retreat_coast" : retreat_coast
            }
        elif move_type == 'D':
            command_data = {
                "id": id,
                "retreat_result": move_type
            }
        else:
            command_data = {
                "id": id,
                "origin_territory": origin_territory,
                "origin_coast": origin_coast,
                "target_territory": target_territory,
                "target_coast": target_coast,
                "supported_territory": supported_territory,
                "supported_coast": supported_coast,
                "convoyed_territory": convoyed_territory,
                "move_type": move_type,
                "submitted": True,
            }
        data.append(command_data)
    return data

class GameInitializationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', TEMPLATE_SETUP)
        call_command('loaddata', VANILLA_UNIT_SETUP)

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

class VanillaAdjudicationTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', TEMPLATE_SETUP)
        call_command('loaddata', VANILLA_UNIT_SETUP)
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

        response = self.client.patch(UPDATE_BULK_ORDER, payload, format="json")
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

class SupportedHoldFails(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', TEMPLATE_SETUP)
        call_command('loaddata', 'tests/json/retreat_setup_1.json')
        cls.user = get_user_model().objects.create_user(username="testuser",password="testpass")

    def test_hold_fail_and_retreat(self):

        """
        France:
            A Ruh S Kie - Mun
            A Kie - Mun
            A Ber S Kie - Mun
        Germany:
            A Mun Holds (so don't need to change anything here...)
            A Boh S Mun H
        """
        # territories = {territory.territory_template.name : territory for territory in Territory.objects.filter(game=game)}
        
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        game = Game.objects.create(name="Test Game")

        orders = {order.origin_territory.territory_template.name : order for order in Order.objects.filter(game=game,turn=game.current_turn)}
        order_ruh = orders["Ruh"]
        order_kie = orders["Kie"]
        order_mun = orders["Mun"]
        order_boh = orders["Boh"]
        order_ber = orders["Ber"]

        orders = [order_ruh, order_kie, order_ber, order_boh, order_mun]

        commands = [
            "A Ruh S Kie - Mun",
            "A Kie - Mun",
            "A Ber S Kie - Mun",
            "A Boh S Mun H"
        ]

        data = orders_to_json(instance=game,commands=commands)
        
        response = self.client.patch(UPDATE_BULK_ORDER, data, format="json")
        self.assertEqual(response.status_code, 200)

        resolve_moves(game)

        for order in orders:
            order.refresh_from_db()
            # print(order)
            if order == order_ruh:
                target = "Mun"
                move = "S"
                result = "SUCCEEDS"
            
            elif order == order_kie:
                target = "Mun"
                move = 'M'
                result = "SUCCEEDS"
            
            elif order == order_ber:
                target = "Mun"
                move = 'S'
                result = 'SUCCEEDS'

            elif order == order_boh:
                target = "Mun"
                move = 'S'
                result = 'SUCCEEDS'
            
            elif order == order_mun:
                target = None
                move = 'H'
                result = 'FAILS'    
            
        if order.target_territory:
            self.assertEqual(order.target_territory.territory_template.name, target)
        self.assertEqual(order.move_type, move)
        self.assertEqual(order.result, result)

        options = UnitRetreatOption.objects.filter(game=game,turn=game.current_turn)
        self.assertEqual(len(options),3)
        self.assertNotEqual(UnitRetreatOption.objects.get(game=game,turn=game.current_turn,territory=Territory.objects.get(game=game,territory_template=TerritoryTemplate.objects.get(name="Tyr"))), None)

        # Test Retreat
        retreat_command = ["A Mun R Tyr"]

        data = orders_to_json(instance=game,commands=retreat_command)
        
        response = self.client.patch(UPDATE_BULK_ORDER, data, format="json")
        self.assertEqual(response.status_code, 200)

        resolve_retreats(game)

        order_mun.refresh_from_db()
        self.assertEqual(order.retreat_territory.territory_template.name, "Tyr")
        self.assertEqual(order.retreat_result, 'R')



class BulkUpdateOrdersTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('loaddata', TEMPLATE_SETUP)
        call_command('loaddata', VANILLA_UNIT_SETUP)
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