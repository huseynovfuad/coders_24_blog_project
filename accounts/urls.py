from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = "accounts"


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("activation/<uuid>/<token>/", views.ActivationView.as_view(), name="activation"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]