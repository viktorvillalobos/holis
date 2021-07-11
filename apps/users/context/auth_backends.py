from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

import logging

from apps.users.context.models import User

logger = logging.getLogger(__name__)


class EmailBackend(ModelBackend):
    def authenticate(self, request, email, password):
        try:
            user = User.objects.get(company=request.company, email=email)
        except User.DoesNotExist:
            logger.info("User does not exists")
            return None

        if check_password(password, user.password):
            return user

        return None
