from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from apps.chat.ws import routing as chat_routing
from apps.core.ws import routing as core_routing

# from apps.core.middleware import TokenAuthMiddleware

websockets = URLRouter(
    [*core_routing.websocket_urlpatterns, *chat_routing.websocket_urlpatterns]
)

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": AuthMiddlewareStack(websockets)
    }
)
