"""
ASGI config for Espazum Remote Team Tool project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""
import os
import sys
from pathlib import Path

import django
from channels.routing import get_default_application

app_path = Path(__file__).parents[1].resolve()
sys.path.append(str(app_path / "apps"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()
application = get_default_application()

