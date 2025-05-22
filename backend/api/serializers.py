from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Game, Territory, Unit, Order, Sandbox

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "email", "username", "password", "pronouns"] # Likely will need more
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class SandboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sandbox
        fields = '__all__'

class TerritorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Territory
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'