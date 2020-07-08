import logging
from apps.users.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

logger = logging.getLogger(__name__)


class EmailBackend(ModelBackend):
    def authenticate(self, request, company_id, email, password):
        logger.info('EMAIL')
        logger.info(email)
        try:
            user = User.objects.get(company_id=company_id, email=email)
        except User.DoesNotExist:
            logger.info('User does not exists')
            return None

        if check_password(password, user.password):
            return user

        return None
