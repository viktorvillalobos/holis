from io import BytesIO
from typing import Dict

import requests
from django.conf import settings
from django.core import files

from .api.serializers import UserSerializer
from .entities import User as UserEntity
from .models import User as UserModel


def get_user(user_id: int) -> UserEntity:
    instance = UserModel.objects.get(id=user_id)
    return UserEntity.load_from_model(instance)


def serialize_user(user: settings.AUTH_USER_MODEL) -> Dict:
    return UserSerializer(user).data


def get_user_avatar_thumb(user: settings.AUTH_USER_MODEL) -> None:
    if not user.avatar:
        url = f"https://avatars.abstractapi.com/v1/?api_key={settings.ABSTRACT_API_KEY}&name={self.username}"  # noqa
        resp = requests.get(url)
        fp = BytesIO()
        fp.write(resp.content)
        file_name = user.username + ".png"
        user.avatar.save(file_name, files.File(fp))
        user.save()

    # return get_thumbnail(self.avatar.file, "100x100", crop="center", quality=99).url
    return user.avatar.url
