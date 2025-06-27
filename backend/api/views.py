from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics
from .models import CustomUser, Game, Territory, Unit, Sandbox, Order
from .serializers import OrderSerializer, TerritorySerializer, UserSerializer, GameSerializer, UnitSerializer, SandboxSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from allauth.account.views import ConfirmEmailView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

# Create your views here.
class ReactConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.confirm(self.request)
        # Replace with actual website later. Assuming Vite using port 5173 but may be a diff port!!!!!!
        return redirect("http://localhost:5173/login") 

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


class BulkUpdateOrdersView(APIView):
    def patch(self, request, *args, **kwargs):
        updates = request.data

        if not isinstance(updates, list):
            return Response({'error' : 'Expected a list of order updates'}, status=status.HTTP_400_BAD_REQUEST)
        
        updated_orders = []

        for order_data in updates:
            order_id = order_data.get('id')
            if not order_id:
                continue

            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                continue # something bad happened

            serializer = OrderSerializer(order, data=order_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_orders.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(updated_orders, status=status.HTTP_200_OK)

class BulkCreateOrders(APIView):
    def patch(self, request, *args, **kwargs):
        orders = request.data

        if not isinstance(orders, list):
            return Response({'error' : 'Expected a list of order updates'}, status=status.HTTP_400_BAD_REQUEST)

        created_orders = []
        for order_data in orders:
            order_id = order_data.get('id')
            if not order_id:
                continue
            order = Order.objects.create(id=order_id)
            serializer = OrderSerializer(order, data=order_data,partial=True)
            if serializer.is_valid():
                serializer.save()
                created_orders.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(created_orders, status=status.HTTP_200_OK)

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
def get_sandbox_by_id(request, pk):
    sandbox = get_object_or_404(Sandbox, pk=pk)
    return Response({
        'id': sandbox.id,
        'creator': sandbox.creator.id,
        'year': sandbox.year,
        'season': sandbox.season
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

