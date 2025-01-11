import os
import asyncio
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Ensure the asyncio event loop is set up before anything else
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ft_transcendence.settings")

# Import routing only after the event loop is set
import transcendence.routing

# Define the ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            transcendence.routing.websocket_urlpatterns
        )
    ),
})

