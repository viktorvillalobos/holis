from typing import List

from celery import shared_task
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from django.core.cache import cache
from django.utils import timezone

import datetime
from channels.layers import get_channel_layer
from datetime import timedelta

from apps.core import services as core_services
from apps.core.channels.utils import force_user_disconect_by_company_and_user_id
from apps.core.lib.constants import USER_POSITION_KEY
from apps.core.models import Company
from apps.users import services as user_services

channel_layer = get_channel_layer()

logger = get_task_logger(__name__)


@periodic_task(run_every=timedelta(minutes=1))
def healtcheck():
    return True


@shared_task
def check_company_areas(company_id: str) -> List[str]:
    logger.info("check_company_areas")

    to_disconnect_user_ids = core_services.get_disconnected_users_ids_by_company_id(
        company_id=company_id
    )

    for user_id, area_id in to_disconnect_user_ids:
        force_user_disconect_by_company_and_user_id(
            company_id=company_id, user_id=user_id
        )

        core_services.remove_user_from_area_by_area_and_user_id(
            area_id=area_id, user_id=user_id
        )

    return to_disconnect_user_ids


@shared_task
def launch_heartbeat_checkers():
    logger.info("check_company_areas")

    # TODO: This should be more specific query

    for company in Company.objects.all():
        check_company_areas.delay(company.id)
