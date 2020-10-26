"""
    This is insane https://gist.github.com/rluts/22e05ed8f53f97bdd02eafdf38f3d60a
"""

import logging

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from rest_framework.authtoken.models import Token

logger = logging.getLogger(__name__)


@database_sync_to_async
def get_user_from_token(token_key):
    if isinstance(token_key, bytes):
        token_key = token_key.decode()  # Dcode if is bytes

    user_from_cache = cache.get(f"ws-{token_key}")

    if user_from_cache:
        logger.info("RETURNING FROM CACHE")
        return user_from_cache

    try:
        user = Token.objects.get(key=token_key).user
        cache.set(f"ws-{token_key}", user, 60 * 60)
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    """
        Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    """

        Yeah, this is black magic:
        https://github.com/django/channels/issues/1399
    """

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    def parse_cookies(self, scope):
        headers = dict(scope["headers"])
        cookie = headers[b"cookie"]
        return {x.split(b"=")[0].strip(): x.split(b"=")[1] for x in cookie.split(b";")}

    async def __call__(self, receive, send):
        cookies = self.parse_cookies(self.scope)
        if b"X-WS-Authorization" in cookies:
            token_key = cookies[b"X-WS-Authorization"]
            self.scope["user"] = await get_user_from_token(token_key)

        inner = self.inner(self.scope)
        return await inner(receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(  # noqa
    AuthMiddlewareStack(inner)
)
