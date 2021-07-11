from typing import Any

from django.core.cache import cache

from apps.core.lib.constants import USER_POSITION_KEY


def get_disconnect_users_ids_by_company_id(company_id) -> dict[str, dict[str, Any]]:
    connected_users_keys = cache.keys(USER_POSITION_KEY.format(company_id, "*"))
    user_positions = cache.get_many(connected_users_keys)

    return user_positions
