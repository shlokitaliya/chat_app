from django.urls import re_path,path

def get_websocket_urlpatterns():
    # ✅ Safe local import after setup is called
    from chat.consumers import ChatConsumer
    return [
        path('ws/chat/<str:room_name>', ChatConsumer.as_asgi()),
    ]

websocket_urlpatterns = get_websocket_urlpatterns()
