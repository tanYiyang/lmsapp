"""
ASGI config for lmsapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lmsapp.settings")
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
import courses.routing
import chat.routing


websocket_urlpatterns = courses.routing.websocket_urlpatterns + chat.routing.websocket_urlpatterns
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
            
        )
    ),
})
