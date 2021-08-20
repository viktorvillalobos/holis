from typing import Any, Dict, Iterable, List, Optional

from django.conf import settings
from django.core import files
from django.core.cache import cache
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

import datetime as dt
import requests
from io import BytesIO

from apps.users.lib.exceptions import UserDoesNotExist
from apps.utils.dataclasses import build_dataclass_from_model_instance

from .api.v100.serializers import UserSerializer
from .context.models import Status, User
from .context.providers import status as status_providers
from .context.providers import user as user_providers
from .lib.constants import USER_NOTIFICATION_CHANNEL_KEY, USER_STATUS_KEY
from .lib.dataclasses import StatusCachedData, UserData


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


def get_user_notification_channel_by_user_id(company_id: int, user_id: int) -> str:
    """ Returns the channel key for notifications """
    return USER_NOTIFICATION_CHANNEL_KEY.format(company_id, user_id)


def touch_user_by_user_and_area_id(user_id: int, area_id: int, ts=None) -> None:
    user_providers.touch_user_by_user_and_area_id(
        user_id=user_id, area_id=area_id, ts=ts
    )


def disconnect_user_by_id(user_id: int) -> None:
    user_providers.disconnect_user_by_id(user_id=user_id)


def set_user_status_by_user_and_status_id(
    company_id: int, user_id: int, status_id: int
) -> None:
    with transaction.atomic():
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


def get_user_active_status_from_db_by_user_id(
    company_id: int, user_id: int
) -> Optional[StatusCachedData]:
    status = status_providers.get_user_active_status_from_db_by_user_id(
        company_id=company_id, user_id=user_id
    )

    if not status:
        return None

    return build_dataclass_from_model_instance(instance=status, klass=StatusCachedData)


def get_user_status_from_anywhere_by_user_id(
    company_id: int, user_id: int
) -> Optional[dict[str, Any]]:
    cached_status = get_user_active_status_from_cache_by_user_id(
        company_id=company_id, user_id=user_id
    )

    if cached_status:
        return cached_status

    status = get_user_active_status_from_db_by_user_id(
        company_id=company_id, user_id=user_id
    )

    if not status:
        return None

    return {"id": status.id, "text": status.text, "icon_text": status.icon_text}


def update_user_profile(
    *,
    id: int,
    company_id: int,
    birthday: dt.datetime,
    email: str,
    name: str,
    position: str,
) -> None:
    """ Update User Profile fields """
    return user_providers.update_user_profile(
        id=id,
        company_id=company_id,
        birthday=birthday,
        email=email,
        name=name,
        position=position,
    )


def get_users_by_ids_in_bulk(
    company_id: int, users_ids: Iterable[int]
) -> dict[int, UserData]:
    """
    Return a Dict with the user id as key and a UserData as value
    """
    users = user_providers.get_users_by_ids(company_id=company_id, users_ids=users_ids)

    return {
        user.id: build_dataclass_from_model_instance(klass=UserData, instance=user)
        for user in users
    }
