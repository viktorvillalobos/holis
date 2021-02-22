from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter

from apps.chat.channels import routing as chat_routing
from apps.core.channels import routing as core_routing

# from apps.core.middleware import TokenAuthMiddleware

websocket_urls = URLRouter(
    [*core_routing.websocket_urlpatterns, *chat_routing.websocket_urlpatterns]
)

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": AuthMiddlewareStack(websocket_urls),
        "http": AsgiHandler(),
    }
)
