from .base import *  # noqa
from .base import LOCAL, ROOT_DIR, env

# GENERAL
# ------------------------------------------------------------------------------

ENVIRONMENT = LOCAL
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="IZGCmcTPYgxBYUDtxH9Dx6NOm0CSoKeZ2x3R4qUssRXSXdH4xGdoECQM9bC8ThQG",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["holis.local", ".holis.local", ".localhost"]

SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", default=True)

SESSION_COOKIE_DOMAIN = env("SESSION_COOKIE_DOMAIN", default=None)

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": "",
#     }
# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            "IGNORE_EXCEPTIONS": True,
        },
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405


# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config


NOT_SHOW_TOOLBAR_IN_URLS = {"/admin", "/app"}


def custom_show_toolbar(request):
    from debug_toolbar.middleware import show_toolbar

    deny = any(request.path.startswith(url) for url in NOT_SHOW_TOOLBAR_IN_URLS)
    return show_toolbar(request) and not deny


DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": False,
    "SHOW_TOOLBAR_CALLBACK": custom_show_toolbar,
}

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# Celery
# ------------------------------------------------------------------------------

# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TASK_ALWAYS_EAGER = True
# Your stuff...
# ------------------------------------------------------------------------------

CORS_ORIGIN_ALLOW_ALL = True


WEBPACK_STATS_FILE = ROOT_DIR / "webapp/webpack-stats.json"

if not WEBPACK_STATS_FILE.exists():
    WEBPACK_STATS_FILE = ROOT_DIR / "webapp/webpack-stats-prod.json"

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "webpack_bundles/",  # must end with slash
        "STATS_FILE": str(WEBPACK_STATS_FILE),
    }
}

EMAIL_RELAY_TOKEN = env("EMAIL_RELAY_TOKEN")
