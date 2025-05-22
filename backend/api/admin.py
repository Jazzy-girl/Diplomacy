from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Game, Territory, Unit, Order
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('pk', 'username', 'email', 'pronouns')

class GameAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Game._meta.fields]

class TerritoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Territory._meta.fields]

class UnitAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Unit._meta.fields]

class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Territory, TerritoryAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Order, OrderAdmin)