from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from apps.core.ws import routing as core_routing


websockets = URLRouter(
    [*core_routing.websocket_urlpatterns]
)

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        'websocket': AuthMiddlewareStack(websockets)
    }
)
