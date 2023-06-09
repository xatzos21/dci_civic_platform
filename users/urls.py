# import django models/libraries
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


# import app modules
from . import views

urlpatterns = [
    # path("register/", views.RegisterUserApiView.as_view(), name="register"),
    path("register/", views.RegisterApiView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("list/", views.UserListView.as_view(), name="user_list"),
    # path("auth/login/", views.LoginView.as_view, name="auth_login"),
    path("follower/", views.FollowUserView.as_view(), name="following"),
    path("profile/<int:pk>", views.UserApiView.as_view(), name="logged-in-profile"),
    path("jwt/create", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
