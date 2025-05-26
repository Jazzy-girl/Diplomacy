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
    year = models.PositiveSmallIntegerField(default=1901)
    season = models.CharField(choices=Seasons.choices, default=Seasons.SPRING)
    def __str__(self):
        return f"{self.id} {self.name}"

class Coasts(models.TextChoices):
    NC = "nc"
    SC = "sc"
    EC = "ec"
    WC = "wc"

class Territory(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    name = models.CharField(max_length=20)
    sc_exists = models.BooleanField(default=False)
    has_coast = models.BooleanField(default=False)

class Unit(models.Model):
    class UnitType(models.TextChoices):
        ARMY = 'A', _('Army')
        FLEET = 'F', _('Fleet')
    
    def __str__(self):
        return f"{self.territory} {self.type}"
        
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    #player id FK
    # territory = models.ForeignKey(Territory, null=True, on_delete=models.SET_NULL)
    territory = models.CharField(max_length=20, null=True)
    type = models.CharField(choices=UnitType.choices)
    owner = models.CharField(choices=[('T', 'Turkey'), ('R', 'Russia')], max_length=1)
    coast = models.CharField(max_length=2, choices=Coasts.choices, null=True, blank=True)

class MoveTypes(models.TextChoices):
    MOVE = 'M', _('Move')
    SUPPORT = 'S', _('Support')
    HOLD = 'H', _('Hold')
    CONVOY = 'C', _('Convoy')
    RETREAT = 'R', _('Retreat')
    BUILD = 'B', _('Build')
    DISBAND = 'D', _('Disband')



class Order(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True, default=None)
    sandbox = models.ForeignKey(Sandbox, on_delete=models.CASCADE, null=True, blank=True, default=None)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="orders_as_unit")
    country = models.CharField(choices=[('T', 'Turkey'), ('R', 'Russia')], max_length=1)
    origin_coast = models.CharField(max_length=2, choices=Coasts.choices, null=True, blank=True) # start coast
    origin_territory = models.CharField(max_length=20) # start territory
    target_territory = models.CharField(max_length=20,null=True,blank=True,default=None) # target territory
    target_coast = models.CharField(max_length=2, choices=Coasts.choices, null=True, blank=True) # target coast
    other_territory = models.CharField(max_length=20, null=True, blank=True, default=None) # territory for support/convoy
    # other_unit for support/convoy unit ID
    other_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, default=None, blank=True, related_name="orders_as_other_unit")
    move_type = models.CharField(choices=MoveTypes.choices, max_length=1)
    year = models.PositiveSmallIntegerField()
    season = models.CharField(choices=Seasons.choices)
    submitted = models.BooleanField(default=False)