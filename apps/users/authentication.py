from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

from users.models import User


class EmailBackend(ModelBackend):
    def authenticate(self, request, company_id, email, password):
        try:
            user = User.objects.get(company_id=company_id, email=email)
        except User.DoesNotExist:
            return None

        if check_password(password, user.password):
            return user

        return None
