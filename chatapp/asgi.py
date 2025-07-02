import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatapp.settings")
django.setup() 

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

print("Loaded WebSocket Routes:")
for r in websocket_urlpatterns:
    print(r)


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )        
    ),
})

