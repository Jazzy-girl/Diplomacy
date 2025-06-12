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
    def __str__(self):
        return f"{self.id} {self.name}"

class Sandbox(models.Model):
    name = models.CharField(max_length=50)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateField("date created", auto_now_add=True)
    turn = models.PositiveSmallIntegerField(default=1)
    # season = models.CharField(choices=Seasons.choices, default=Seasons.SPRING)
    def __str__(self):
        return f"{self.id} {self.name}"

class Coasts(models.TextChoices):
    NC = "nc"
    SC = "sc"
    EC = "ec"
    WC = "wc"


class Country(models.Model):
    name = models.CharField(max_length=3)
    full_name = models.CharField(max_length=80)
class TerritoryTemplate(models.Model):
    class TerritoryTypes(models.TextChoices):
        SEA = 'S', _('sea')
        LAND = 'L', _('land')
        COAST = 'C', _('coast')
    name = models.CharField(max_length=3)
    full_name = models.CharField(max_length=80)
    sc_exists = models.BooleanField(default=False)
    territory_type = models.CharField(choices=TerritoryTypes.choices)
    has_coasts = models.BooleanField(default=False)
class TerritoryCoastTemplate(models.Model):
    """
    One to Many relationship table connecting coasts to territories.
    """
    territory = models.ForeignKey(TerritoryTemplate, on_delete=models.CASCADE, related_name='template_as_territory')
    coast = models.ForeignKey(TerritoryTemplate, on_delete=models.CASCADE, related_name='template_as_coast')

class Territory(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    territory_template = models.ForeignKey(TerritoryTemplate, on_delete=models.CASCADE, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, default=None)

class Unit(models.Model):
    class UnitType(models.TextChoices):
        ARMY = 'A', _('Army')
        FLEET = 'F', _('Fleet')
    
    def __str__(self):
        return f"{self.territory} {self.type}"
        
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    disbanded = models.BooleanField(default=False)
    # territory = models.ForeignKey(Territory, null=True, on_delete=models.SET_NULL)
    territory = models.CharField(max_length=20, null=True)
    type = models.CharField(choices=UnitType.choices)
    owner = models.CharField(choices=[('T', 'Turkey'), ('R', 'Russia')], max_length=1)
    coast = models.CharField(max_length=2, choices=Coasts.choices, null=True, blank=True)

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
    country = models.CharField(choices=[('T', 'Turkey'), ('R', 'Russia')], max_length=1)
    origin_territory = models.CharField(max_length=20) # start territory
    target_territory = models.CharField(max_length=20,null=True,blank=True,default=None) # target territory
    supported_territory = models.CharField(max_length=20, null=True, blank=True, default=None) # territory for support
    convoyed_territory = models.CharField(max_length=20, null=True, blank=True, default=None) # territory for convoy
    move_type = models.CharField(choices=MoveTypes.choices, max_length=1, null=True, blank=True, default=None)
    turn = models.PositiveSmallIntegerField(default=1)
    submitted = models.BooleanField(default=False)
    result = models.CharField(choices=OrderResult.choices, max_length=10)
    fail_reason = models.ForeignKey(FailureReason, on_delete=models.SET_NULL, null=True)
    dislodged = models.BooleanField(default=False)
    retreat_required = models.BooleanField(default=False)
    # retreat_territory = models.ForeignKey()
    retreat_result = models.CharField(RetreatResult.choices, max_length=7, null=True, blank=True, default=None) # RETREAT, DISBAND
    # build_territory FK opt
    winter_order = models.CharField(WinterMoveTypes.choices, max_length=7, null=True, blank=True, default=None)