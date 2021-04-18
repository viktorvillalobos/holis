from django.conf import settings
from django.core.cache import caches
from django.db.models import Model, QuerySet

import logging
import random
import threading
from hashlib import sha1
from pickle import UnpicklingError  # nosec import for error handling only

logger = logging.getLogger(__name__)

globals = threading.local()


DAY = 60 * 60 * 24


def cache(seconds, criteria=None, backend="default", jittering_pctg=None):
    def do_cache(f):
        def x(*args, **kwargs):
            # clean arguments
            if settings.ENVIRONMENT == "testing":
                return f(*args, **kwargs)
            else:
                cleaned_args = []
                for arg in args:
                    if isinstance(arg, Model):
                        cleaned_args.append("{}-{}".format(arg.__class__, arg.pk))
                    else:
                        cleaned_args.append("{}".format(arg))

                # generate a key for the method called, using the arguments
                pre_key = "{}{}{}{}".format(
                    f.__module__, f.__name__, tuple(cleaned_args), kwargs
                ).encode("utf-8")
                key = sha1(bytes(pre_key)).hexdigest()

                # we have caching at request level and Redis-level, the
                # request-level cache don't exist outside the request context
                # (i.e. celery tasks, commands, tests)
                request_cache_exists = hasattr(globals, "request_cache")

                if request_cache_exists and key in globals.request_cache:
                    # if the request-cache level is available, and the key
                    # exists then return the stored object for that key
                    return globals.request_cache[key]

                django_cache = caches[backend]

                try:
                    result = django_cache.get(key)
                except (ValueError, UnpicklingError):
                    django_cache.delete(key)
                    logger.warning(
                        "Unexpected data when accessing cache key %s, cache value has been deleted",
                        key,
                        exc_info=True,
                    )
                    result = None

                if result is not None:
                    if request_cache_exists:
                        # if the object exists at Redis level, store the
                        # object at a request level if available
                        globals.request_cache[key] = result
                else:
                    # this means neither the request-level or the Redis-level
                    # cache have the object stored for that key
                    result = f(*args, **kwargs)

                    queryset_in_result = isinstance(result, QuerySet)
                    queryset_in_args = any(isinstance(arg, QuerySet) for arg in args)
                    queryset_in_kwargs = any(
                        isinstance(arg, QuerySet) for arg in kwargs.values()
                    )
                    if queryset_in_result or queryset_in_args or queryset_in_kwargs:
                        logger.warning(
                            "Trying to store a QuerySet instance in cache",
                            exc_info=True,
                        )

                    if not criteria or criteria(result):
                        # if the criteria is met, then store in both levels of cache the object
                        cache_duration = seconds

                        if jittering_pctg is not None:
                            cache_duration -= int(
                                random.random() * cache_duration * jittering_pctg
                            )

                        django_cache.set(key, result, cache_duration)

                        if request_cache_exists:
                            globals.request_cache[key] = result
                return result

        return x

    return do_cache
