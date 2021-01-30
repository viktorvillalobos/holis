from typing import List

from django.db.models import Count
from ..models import Room

from apps.utils.cache import cache


# @cache(60 * 60 * 24)
def get_one_to_one_room_by_members_ids(company_id: int, members_ids: List[int]) -> Room:
    return (
        Room.objects.filter(
            company_id=company_id, members__id__in=members_ids, is_one_to_one=True
        )
        .annotate(num_members=Count("members"))
        .filter(num_members=2)
        .earliest("created")
    )
