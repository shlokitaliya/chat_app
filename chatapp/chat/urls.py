from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('add_friend', views.add_friend, name='add_friend'),
    path('fetch_messages/<int:friend_id>', views.fetch_private_messages, name="fetch_private_messages"),
    path('profile', views.profile_view, name ="profile_view")
]