"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from requests import Response
from api.views import CreateUserView, ReactConfirmEmailView, current_user, get_user_by_id, update_user, GameList, TerritoryList, UnitList, CreateGameView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response

# class EmailVerificationSentAPIView(APIView):
#     def get(self, request):
#         return Response({"detail": "Verification email sent."})
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path('accounts/', include('allauth.urls')),
        path(
        'dj-rest-auth/registration/account-confirm-email/<str:key>/',
        ReactConfirmEmailView.as_view(),
        name='account_confirm_email',
    ),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path('api/user/', current_user, name='current_user'),
    path('api/user/update/', update_user, name='update_user'),
    path('api/user/<int:pk>/', get_user_by_id, name='get_user_by_id'),
    # Game related
    path('api/games/list/', GameList.as_view(), name="game-list"),
    path('api/games/create/', CreateGameView.as_view(), name="game-create"),
    path('api/territories/list/', TerritoryList.as_view(), name="territory-list"),
    path('api/units/list/', UnitList.as_view(), name="unit-list"),
    
]
