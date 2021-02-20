from typing import Dict, List

from django.conf import settings
from django.core import files
from django.db.models import Q
from django.utils import timezone

import datetime as dt
import requests
from io import BytesIO

from .api.serializers import UserSerializer
from .lib.dataclasses import User as UserEntity
from .models import User


def get_user(user_id: int) -> UserEntity:
    instance = User.objects.get(id=user_id)
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


def get_unavailable_users_by_company_id(company_id: int) -> List[User]:
    """ Return a list of ids of users who haven't sent hearbeat check """

    return list(
        User.objects.filter(company_id=company_id)
        .filter(last_seen__lt=timezone.now() - dt.timedelta(seconds=60))
        .exclude(Q(last_seen=None) | Q(current_area=None))
    )


def get_user_notification_channel_by_user_id(user_id: int) -> str:
    """ Returns the channel key for notifications """
    return f"notification-{user_id}"
