from apps.core.ws import routing as core_routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# from apps.core.middleware import TokenAuthMiddleware

websockets = URLRouter([*core_routing.websocket_urlpatterns])

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": AuthMiddlewareStack(websockets)
    }
)
