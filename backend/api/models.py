from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False)
    pronouns = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

    def __str__(self):
        return f"{self.username} {self.email}"
class Seasons(models.TextChoices):
    FALL = 'fall', _('Fall')
    SPRING = 'spring', _('Spring')
    WINTER = 'winter', _('Winter')
class Game(models.Model):
    class PressOptions(models.TextChoices):
        DEFAULT = 'default' # Allowed except for Winter & Retreats
        ALWAYS = 'always' # Always
        GUNBOAT = 'gunboat' # Gunboat -- no press whatsoever
        WILSON = 'wilson' # All press is sent to everyone
    
    class GameType(models.TextChoices):
        PUBLIC = 'public'
        PRIVATE = 'private'
    
    class AdjudicationLength(models.TextChoices):
        MINUTES = 'minutes'
        HOURS = 'hours'
        DAYS = 'days'
    
    class TimeZone(models.TextChoices):
        # There's a lot of time zones.... is there a better way to do this??
        US_PACIFIC = 'us_pt'
        US_EAST = 'us_et'

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, default="")
    current_turn = models.PositiveSmallIntegerField(default=0)
    retreat_required = models.BooleanField(default=False)
    creator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, default=None, blank=True, related_name="customuser_as_creator")
    created_date = models.DateField("date created", auto_now_add=True)
    full = models.BooleanField(default=False)
    next_adjudication = models.DateField("next adjudication", null=True, blank=True, default=None)
    adjudicating = models.BooleanField(default=False)
    gm = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name="customuser_as_gm")

    # DELETE THIS LATER
    _settings_dict = {
        "type": GameType.PUBLIC,
        "press": PressOptions.DEFAULT,
        "adjudication": {
            "regular_unit": AdjudicationLength.DAYS,
            "spring_fall": 1,
            "winter_retreat": 50,
            "first_unit": AdjudicationLength.DAYS,
            "first_turn": 7,
            "start": 12, # Hour; 00 to 24
            "time_zone": TimeZone.US_EAST
        }
    }

    settings = models.JSONField(default=dict(_settings_dict))

    def __str__(self):
        return f"{self.creator} {self.name}"

class PlayersGames(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Sandbox(models.Model):
    name = models.CharField(max_length=50)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateField("date created", auto_now_add=True)
    current_turn = models.PositiveSmallIntegerField(default=0)
    retreat_required = models.BooleanField(default=False)
    adjudicating = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.id} {self.name}"

class CountryTemplate(models.Model):
    name = models.CharField(max_length=3)
    full_name = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.full_name}"

class Country(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    country_template = models.ForeignKey(CountryTemplate, on_delete=models.CASCADE)
    scs = models.IntegerField(default=0)
    available_builds = models.PositiveSmallIntegerField(default=0)
    needed_disbands = models.PositiveSmallIntegerField(default=0)
    submitted_orders = models.BooleanField(default=False)

    def __str__(self):
        return self.country_template.__str__()

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
    home_center = models.BooleanField(default=False)

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

    def __str__(self):
        return self.territory_template.full_name

class Unit(models.Model):
    
    def __str__(self):
        return f"{self.type} {self.coast.full_name if self.coast else self.territory.territory_template.full_name}"
        
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
    
    class AdjustmentTypes(models.TextChoices):
        BUILD = 'B', _('Build')
        DISBAND = 'D', _('Disband')

    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    # unit_type = models.CharField(choices=UnitType, max_length=1)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="orders_as_unit", blank=True, null=True, default=None)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    origin_territory = models.ForeignKey(Territory, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="orders_as_origin_territory") # start territory
    origin_coast = models.ForeignKey(CoastTemplate, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="orders_as_origin_coast")
    target_territory = models.ForeignKey(Territory, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="orders_as_target_territory") # target territory
    target_coast = models.ForeignKey(CoastTemplate, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="orders_as_target_coast")
    supported_territory = models.ForeignKey(Territory, on_delete=models.CASCADE,null=True, blank=True, default=None, related_name="orders_as_supported_territory") # territory for support
    supported_coast = models.ForeignKey(CoastTemplate, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="orders_as_supported_coast")
    convoyed_territory = models.ForeignKey(Territory, on_delete=models.CASCADE,null=True, blank=True, default=None, related_name="orders_as_convoyed_territory") # territory for convoy
    move_type = models.CharField(choices=MoveTypes.choices, max_length=1, null=True, blank=True, default=None)
    turn = models.PositiveSmallIntegerField(default=0)
    submitted = models.BooleanField(default=False)
    result = models.CharField(choices=OrderResult.choices, max_length=10, default='PENDING')
    fail_reason = models.ForeignKey(FailureReason, on_delete=models.SET_NULL, null=True, blank=True,default=None)
    dislodged = models.BooleanField(default=False)
    retreat_required = models.BooleanField(default=False)
    retreat_territory = models.ForeignKey(Territory, on_delete=models.CASCADE,null=True, blank=True, default=None, related_name="orders_as_retreat_territory") # territory for support
    retreat_coast = models.ForeignKey(CoastTemplate, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="orders_as_retreat_coast")
    retreat_result = models.CharField(RetreatResult.choices, max_length=7, null=True, blank=True, default=None) # RETREAT, DISBAND
    build_territory = models.ForeignKey(Territory, on_delete=models.CASCADE,null=True, blank=True, default=None, related_name="orders_as_build_territory")
    build_coast = models.ForeignKey(CoastTemplate, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="orders_as_build_coast")
    build_type = models.CharField(choices=UnitType, max_length=1,null=True, blank=True, default=None)
    adjustment_type = models.CharField(AdjustmentTypes.choices, max_length=7, null=True, blank=True, default=None)

    def __str__(self):
        if self.move_type:
            match self.move_type:
                case 'M' | 'V':
                    return f"{self.unit} {self.move_type} {self.target_coast or self.target_territory} {self.result}"
                case 'H':
                    return f"{self.unit} {self.move_type} {self.result}"
                case 'S':
                    return f"{self.unit} {self.move_type} {self.supported_coast or self.supported_territory} - {self.target_coast or self.target_territory} {self.result}"
                case _:
                    return super().__str__()
        elif self.adjustment_type:
            match self.adjustment_type:
                case 'B':
                    return f"{self.build_type} BUILD {self.build_coast or self.build_territory} {self.result}"
                case 'D':
                    return f"{self.unit} DISBANDS {self.result}"
                case _:
                    return super().__str__()
        else:
            return super().__str__()
            
class UnitRetreatOption(models.Model):
    # unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)
    coast = models.ForeignKey(CoastTemplate, on_delete=models.CASCADE, default=None,null=True,blank=True)
    turn = models.PositiveSmallIntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.order.unit} : {self.coast.full_name if self.coast else self.territory.territory_template.full_name}"
    
class AdjustmentCache(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    build_cache = models.JSONField(null=True,blank=True,default=None)
    disband_cache = models.JSONField(null=True,blank=True,default=None)
    turn = models.PositiveSmallIntegerField()

class TerritoryCountrySnapshot(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, default=None)
    turn = models.PositiveSmallIntegerField()
    

class CountrySCCountSnapshot(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)    
    scs = models.PositiveSmallIntegerField()
    turn = models.PositiveSmallIntegerField()

class UnitLocationSnapshot(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)
    coast = models.ForeignKey(CoastTemplate, on_delete=models.CASCADE,null=True,blank=True,default=None)
    turn = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.unit.country} {self.unit.type} {self.coast or self.territory}"

class Chain(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    title = models.TextField()
    last_updated = models.DateTimeField("date created", default=timezone.now)

    def __str__(self):
        return f"{self.title}, last updated: {self.last_updated}"

class Message(models.Model):
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField("date created", auto_now_add=True)

    def __str__(self):
        return f"{self.country}: {self.text}"

class CountryChain(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    chain = models.ForeignKey(Chain, on_delete=models.CASCADE)
    unread = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.chain} : {self.country} {"UNREAD" if self.unread else "READ"}"