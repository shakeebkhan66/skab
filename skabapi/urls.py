from django.urls import path
from skabapi.views import RegisterAPIView, Recipes, CreateRecipes, LoginView, UserProfileView, \
    UserChangePasswordView, SendPasswordResetEmailView, ResetPasswordSubmitView, LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # path('api/login/', TokenObtainPairView.as_view(), name='token_view'),
    path('api/login/', LoginView.as_view(), name='login_view'),
    path('api/register/', RegisterAPIView.as_view(), name='register_view'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),
    path('api/change_password/', UserChangePasswordView.as_view(), name='change_password'),
    path('api/send_password_reset_email/', SendPasswordResetEmailView.as_view(), name='send_password_reset_email'),
    path('api/reset_password/<uid>/<token>/', ResetPasswordSubmitView.as_view(), name='reset_password'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('api/allrecipes/', Recipes.as_view(), name='all_recipes'),
    path('api/createrecipe/', CreateRecipes.as_view(), name='create_recipe')
]