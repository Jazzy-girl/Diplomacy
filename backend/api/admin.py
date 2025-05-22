from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Game, Territory, Unit, Order
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('pk', 'username', 'email', 'pronouns')

class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class TerritoryAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "name", "sc_exists")

class UnitAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "location", "type", "owner")

class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Territory, TerritoryAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Order, OrderAdmin)