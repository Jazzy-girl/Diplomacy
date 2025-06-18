from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False)
    pronouns = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

    def __str__(self):
        return self.email
class Seasons(models.TextChoices):
    FALL = 'fall', _('Fall')
    SPRING = 'spring', _('Spring')
    WINTER = 'winter', _('Winter')
class Game(models.Model):
    name = models.CharField(max_length=50)
    current_turn = models.PositiveSmallIntegerField(default=1)
    def __str__(self):
        return f"{self.id} {self.name}"

class Sandbox(models.Model):
    name = models.CharField(max_length=50)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateField("date created", auto_now_add=True)
    current_turn = models.PositiveSmallIntegerField(default=1)
    def __str__(self):
        return f"{self.id} {self.name}"

class CountryTemplate(models.Model):
    name = models.CharField(max_length=3)
    full_name = models.CharField(max_length=80)
    scs = models.PositiveSmallIntegerField(default=3)

    def __str__(self):
        return f"{self.full_name}"

class Country(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    country_template = models.ForeignKey(CountryTemplate, on_delete=models.CASCADE)
    scs = models.IntegerField(default=0)

class UnitType(models.TextChoices):
    ARMY = 'A', _('Army')
    FLEET = 'F', _('Fleet')

class TerritoryTemplate(models.Model):
    class TerritoryTypes(models.TextChoices):
        SEA = 'S', _('sea')
        LAND = 'L', _('land')
    name = models.CharField(max_length=6)
    full_name = models.CharField(max_length=80)
    sc_exists = models.BooleanField(default=False)
    territory_type = models.CharField(choices=TerritoryTypes.choices)
    has_coasts = models.BooleanField(default=False)
    country_template = models.ForeignKey(CountryTemplate, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.full_name}"

class CoastTemplate(models.Model):
    territory_template = models.ForeignKey(TerritoryTemplate, on_delete=models.CASCADE)
    name = models.CharField(max_length=6)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name}"

class InitialUnitSetup(models.Model):
    territory_template = models.ForeignKey(TerritoryTemplate, on_delete=models.CASCADE)
    country_template = models.ForeignKey(CountryTemplate, on_delete=models.CASCADE)
    unit_type = models.CharField(choices=UnitType.choices, max_length=1, null=True, blank=True, default=None)
    coast_template = models.ForeignKey(CoastTemplate, on_delete=models.CASCADE, null=True, blank=True, default=None)

class Territory(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    territory_template = models.ForeignKey(TerritoryTemplate, on_delete=models.CASCADE, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, default=None)

class Unit(models.Model):
    
    def __str__(self):
        return f"{self.territory} {self.type}"
        
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    disbanded = models.BooleanField(default=False)
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)
    type = models.CharField(choices=UnitType.choices, max_length=1)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    coast = models.ForeignKey(CoastTemplate, on_delete=models.CASCADE, null=True, blank=True, default=None)
class FailureReason(models.Model):
    reason = models.TextField()

class Order(models.Model):
    class MoveTypes(models.TextChoices):
        MOVE = 'M', _('Move')
        MOVE_VIA_CONVOY = 'V', _('Move via Convoy')
        SUPPORT = 'S', _('Support')
        HOLD = 'H', _('Hold')
        CONVOY = 'C', _('Convoy')

    class OrderResult(models.TextChoices):
        PENDING = 'PENDING'
        SUCCEEDS = 'SUCCEEDS'
        FAILS = 'FAILS'

    class RetreatResult(models.TextChoices):
        RETREAT = 'R', _('Retreat')
        DISBAND = 'D', _('Disband')
    
    class WinterMoveTypes(models.TextChoices):
        BUILD = 'B', _('Build')
        DISBAND = 'D', _('Disband')

    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="orders_as_unit", null=True, default=None)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    origin_territory = models.ForeignKey(Territory, on_delete=models.CASCADE, related_name="orders_as_origin_territory") # start territory
    origin_coast = models.ForeignKey(CoastTemplate, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="orders_as_origin_coast")
    target_territory = models.ForeignKey(Territory, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="orders_as_target_territory") # target territory
    target_coast = models.ForeignKey(CoastTemplate, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="orders_as_target_coast")
    supported_territory = models.ForeignKey(Territory, on_delete=models.CASCADE,null=True, blank=True, default=None, related_name="orders_as_supported_territory") # territory for support
    supported_coast = models.ForeignKey(CoastTemplate, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="orders_as_supported_coast")
    convoyed_territory = models.ForeignKey(Territory, on_delete=models.CASCADE,null=True, blank=True, default=None, related_name="orders_as_convoyed_territory") # territory for convoy
    move_type = models.CharField(choices=MoveTypes.choices, max_length=1, null=True, blank=True, default=None)
    turn = models.PositiveSmallIntegerField(default=1)
    submitted = models.BooleanField(default=False)
    result = models.CharField(choices=OrderResult.choices, max_length=10, default='PENDING')
    fail_reason = models.ForeignKey(FailureReason, on_delete=models.SET_NULL, null=True)
    dislodged = models.BooleanField(default=False)
    retreat_required = models.BooleanField(default=False)
    retreat_territory = models.ForeignKey(Territory, on_delete=models.CASCADE,null=True, blank=True, default=None, related_name="orders_as_retreat_territory") # territory for support
    retreat_coast = models.ForeignKey(CoastTemplate, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="orders_as_retreat_coast")
    retreat_result = models.CharField(RetreatResult.choices, max_length=7, null=True, blank=True, default=None) # RETREAT, DISBAND
    build_territory = models.ForeignKey(Territory, on_delete=models.CASCADE,null=True, blank=True, default=None, related_name="orders_as_build_territory")
    winter_order = models.CharField(WinterMoveTypes.choices, max_length=7, null=True, blank=True, default=None)