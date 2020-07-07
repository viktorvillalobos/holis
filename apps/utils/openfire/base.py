import logging

from django.conf import settings

from .exceptions import (
    AlreadyExistsException,
    GroupAlreadyExistsException,
    GroupNotFoundException,
    IllegalArgumentException,
    InvalidResponseException,
    NotAllowedException,
    PropertyNotFoundException,
    RequestNotAuthorisedException,
    RoomNotFoundException,
    SharedGroupException,
    UserAlreadyExistsException,
    UserNotFoundException,
    UserServiceDisabledException,
)

EXCEPTIONS_MAP = {
    "IllegalArgumentException": IllegalArgumentException,
    "UserNotFoundException": UserNotFoundException,
    "UserAlreadyExistsException": UserAlreadyExistsException,
    "RequestNotAuthorised": RequestNotAuthorisedException,
    "UserServiceDisabled": UserServiceDisabledException,
    "SharedGroupException": SharedGroupException,
    "PropertyNotFoundException": PropertyNotFoundException,
    "GroupAlreadyExistsException": GroupAlreadyExistsException,
    "GroupNotFoundException": GroupNotFoundException,
    "RoomNotFoundException": RoomNotFoundException,
    "NotAllowedException": NotAllowedException,
    "AlreadyExistsException": AlreadyExistsException,
}

logger = logging.getLogger(__name__)


class Base(object):
    def __init__(self, host=None, secret=None, endpoint=None):
        """
        :param host: Scheme://Host/ for API requests
        :param secret: Shared secret key for API requests
        :param endpoint: Endpoint for API requests
        """
        self.headers = {}
        self.headers["Authorization"] = secret or settings.OPENFIRE_SECRET
        self.headers["Accept"] = "application/json"
        self.host = host or settings.OPENFIRE_HOST
        self.endpoint = endpoint

    def _submit_request(self, func, endpoint, **kwargs):
        """
        Wrapper for send a request
        :param func: Name of the function for request
        :param endpoint: Plugin endpoint for request
        :param **kwargs: Arguments that request takes
        :return: JSON object or True
        """
        r = func(headers=self.headers, url=self.host + endpoint, **kwargs)
        if r.status_code in (200, 201):
            try:
                return r.json()
            except Exception:
                return True
        else:
            try:
                logger.info("-------------------LOGGER")
                logger.info(r.content)
                exception = r.json()["exception"]
                message = r.json()["message"]
            except Exception:
                raise InvalidResponseException(r.status_code)
            if exception in EXCEPTIONS_MAP:
                raise EXCEPTIONS_MAP[exception](message)
            else:
                raise InvalidResponseException(exception)
