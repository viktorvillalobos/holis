"""
ASGI config for Holis Remote Team Tool project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""
import django
from django.conf import settings

import os
import sentry_sdk
import sys
from channels.routing import get_default_application
from pathlib import Path
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

app_path = Path(__file__).parents[1].resolve()
sys.path.append(str(app_path / "apps"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()


application = get_default_application()

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[settings.SENTRY_LOGGING, DjangoIntegration(), CeleryIntegration()],
)
application = SentryAsgiMiddleware(application)
