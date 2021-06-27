"""
With these settings, tests run faster.
"""

from .base import *  # noqa
from .base import DATABASES, TESTING, env

# GENERAL
# ------------------------------------------------------------------------------

ENVIRONMENT = TESTING

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="DdfWfnQ5Xuu2S0aJZLseZfEUGQjboYZY0b94sgSA6AzFiIj6YJ00qLOCHbBXU7mQ",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

DATABASES["default"]["NAME"] = "holis"
DATABASES["default"]["USER"] = "root"
DATABASES["default"]["PASSWORD"] = "root"
DATABASES["default"]["HOST"] = "postgres"
DATABASES["default"]["PORT"] = "26257"
DATABASES["default"]["OPTIONS"] = {}

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES[-1]["OPTIONS"]["loaders"] = [  # type: ignore[index] # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Your stuff...
# ------------------------------------------------------------------------------
