from django.urls import path
from skabapi.views import RegisterAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_view'),
    path('api/register/', RegisterAPIView.as_view(), name='register_view'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
]