from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Game, Territory, Unit, Order, Sandbox, TerritoryTemplate, Country, CountryTemplate, CoastTemplate, InitialUnitSetup
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('pk', 'username', 'email', 'pronouns')

class GameAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Game._meta.fields]

class SandboxAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Sandbox._meta.fields]

class TerritoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Territory._meta.fields]

class TerritoryTemplateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TerritoryTemplate._meta.fields]

class CoastTemplateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CoastTemplate._meta.fields]

class UnitAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Unit._meta.fields]

class CountryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Country._meta.fields]

class CountryTemplateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CountryTemplate._meta.fields]

class InitialUnitSetupAdmin(admin.ModelAdmin):
    list_display = [field.name for field in InitialUnitSetup._meta.fields]

class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Territory, TerritoryAdmin)
admin.site.register(TerritoryTemplate, TerritoryTemplateAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(CountryTemplate, CountryTemplateAdmin)
admin.site.register(CoastTemplate, CoastTemplateAdmin)
admin.site.register(InitialUnitSetup, InitialUnitSetupAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Sandbox, SandboxAdmin)