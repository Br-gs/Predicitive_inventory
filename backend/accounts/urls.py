from django.urls import path, include
from .user_api import RegisterView, UserDetailView, ChangePasswordView, LogoutView, UserListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'accounts'

urlpatterns = [
    # API endpoints for JWT authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

    # API endpoints for user registration and profile management
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/user/profile/', UserDetailView.as_view(), name='user_profile'),
    path('api/user/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/users/', UserListView.as_view(), name='user_list'),]