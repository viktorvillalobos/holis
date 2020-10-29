from typing import Dict

from django.conf import settings

from .api.serializers import UserSerializer
from .entities import User as UserEntity
from .models import User as UserModel


def get_user(user_id: int) -> UserEntity:
    instance = UserModel.objects.get(id=user_id)
    return UserEntity.load_from_model(instance)


def serialize_user(user: settings.AUTH_USER_MODEL) -> Dict:
    return UserSerializer(user).data
