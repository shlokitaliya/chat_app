from chat.consumers import ChatConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/socket_server/', ChatConsumer.as_asgi()),
]