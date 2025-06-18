from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("signup/", views.signup_view, name="signup_view"),
]