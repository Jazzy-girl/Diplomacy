from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from allauth.account.views import ConfirmEmailView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
            'username': user.username,
            'email': user.email,
            'pronouns': user.pronouns,
        })

class ReactConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.confirm(self.request)
        return redirect("http://localhost:5173/login") # Replace with actual website later. Assuming Vite using 5173