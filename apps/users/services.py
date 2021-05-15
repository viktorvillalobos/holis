from typing import Any, Dict, List, Optional

from django.conf import settings
from django.core import files
from django.core.cache import cache
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

import datetime as dt
import requests
from io import BytesIO

from .api.serializers import UserSerializer
from .lib.constants import USER_STATUS_KEY
from .lib.dataclasses import StatusCachedData
from .lib.dataclasses import User as UserEntity
from .models import Status, User
from .providers import status as status_providers
from .providers import user as user_providers


def get_user(user_id: int) -> UserEntity:
    instance = User.objects.get(id=user_id)
    return UserEntity.load_from_model(instance)


def serialize_user(user: settings.AUTH_USER_MODEL) -> Dict:
    return UserSerializer(user).data


def get_user_avatar_thumb(user: settings.AUTH_USER_MODEL) -> None:
    if not user.avatar:
        url = f"https://avatars.abstractapi.com/v1/?api_key={settings.ABSTRACT_API_KEY}&name={user.username}"  # noqa
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
        User.objects.filter(company_id=company_id).filter(
            Q(last_seen__lt=timezone.now() - dt.timedelta(seconds=60))
            | Q(current_area=None)
        )
    )


def get_user_notification_channel_by_user_id(user_id: int) -> str:
    """ Returns the channel key for notifications """
    return f"notification-{user_id}"


def touch_user_by_user_and_area_id(user_id: int, area_id: int, ts=None) -> None:
    user_providers.touch_user_by_user_and_area_id(
        user_id=user_id, area_id=area_id, ts=ts
    )


def disconnect_user_by_id(user_id: int) -> None:
    user_providers.disconnect_user_by_id(user_id=user_id)


def set_user_status_by_user_and_status_id(
    company_id: int, user_id: int, status_id: int
) -> None:
    with transaction.atomic:
        status_providers.inactivate_all_user_status_by_user_id(
            company_id=company_id, user_id=user_id
        )

        status_providers.set_active_status_by_user_and_status_id(
            company_id=company_id, user_id=user_id, status_id=status_id
        )


def get_user_active_status_from_cache_by_user_id(
    company_id: int, user_id: int
) -> Optional[dict[str, Any]]:
    return status_providers.get_user_active_status_from_cache_by_user_id(
        company_id=company_id, user_id=user_id
    )
