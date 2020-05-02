"""
ASGI config for Lesgens Remote Team Tool project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""
import os
import sys
from pathlib import Path

# from django.core.asgi import get_asgi_application
import django
from channels.routing import get_default_application
# This allows easy placement of apps within the interior
# lesgens directory.
app_path = Path(__file__).parents[1].resolve()
sys.path.append(str(app_path / "lesgens"))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()
application = get_default_application()

# This application object is used by any ASGI server configured to use this file.
# django_application = get_asgi_application()
# Apply ASGI middleware here.
# from helloworld.asgi import HelloWorldApplication
# application = HelloWorldApplication(application)

# Import websocket application here, so apps from django_application are loaded first
# from config.websocket import websocket_application  # noqa isort:skip


# async def application(scope, receive, send):
#     if scope["type"] == "http":
#         await django_application(scope, receive, send)
#     elif scope["type"] == "websocket":
#         await websocket_application(scope, receive, send)
#     else:
#         raise NotImplementedError(f"Unknown scope type {scope['type']}")
