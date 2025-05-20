from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False)
    pronouns = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

    def __str__(self):
        return self.email
class Game(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.id} {self.name}"
class Territory(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    sc_exists = models.BooleanField(default=False)
    retreating_unit = models.ForeignKey("Unit", null=True, on_delete=models.SET_NULL)
class Unit(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    #player id FK
    location = models.ForeignKey(Territory, null=True, on_delete=models.SET_NULL)
    type = models.CharField(choices=[('A', 'Army'), ('F', 'Fleet')], max_length=1)
    owner = models.CharField(choices=[('T', 'Turkey'), ('R', 'Russia')], max_length=1)