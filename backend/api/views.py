from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics
from .models import CustomUser, Game, Territory, Unit, Sandbox
from .serializers import TerritorySerializer, UserSerializer, GameSerializer, UnitSerializer, SandboxSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from allauth.account.views import ConfirmEmailView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import viewsets
# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CreateGameView(generics.CreateAPIView):
    queryset = Game.objects.all()
    serializer_class=GameSerializer
    permission_classes = [AllowAny]
class GameList(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [AllowAny]

class CreateSandboxView(generics.CreateAPIView):
    queryset = Sandbox.objects.all()
    serializer_class=SandboxSerializer
    permission_classes = [AllowAny]
class SandboxList(generics.ListAPIView):
    queryset = Sandbox.objects.all()
    serializer_class = SandboxSerializer
    permission_classes = [AllowAny]

class TerritoryList(generics.ListAPIView):
    queryset = Territory.objects.all()
    serializer_class = TerritorySerializer
    permission_classes = [AllowAny]

class UnitList(generics.ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'pronouns': user.pronouns,
        })

@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def get_user_by_id(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return Response({
            'username': user.username,
            'email': user.email,
            'pronouns': user.pronouns,
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

class ReactConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.confirm(self.request)
        return redirect("http://localhost:5174/login") # Replace with actual website later. Assuming Vite using 5173