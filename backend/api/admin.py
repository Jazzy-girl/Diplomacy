from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Game
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('pk', 'username', 'email', 'pronouns')

class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Game, GameAdmin)