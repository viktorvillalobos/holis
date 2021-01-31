from celery import shared_task
from celery.utils.log import get_task_logger

from channels.layers import get_channel_layer

from apps.core import services as core_services
from apps.core.models import Company
from apps.core.ws.utils import force_user_disconect_by_company_and_user_id
from apps.users import services as user_services

channel_layer = get_channel_layer()

logger = get_task_logger(__name__)


@shared_task
def check_company_areas(company_id: str) -> None:
    company = Company.objects.get(id=company_id)
    logger.info("check_company_areas")

    result = []

    unavailable_users = user_services.get_unavailable_users_by_company_id(
        company_id=company_id
    )

    for user in unavailable_users:
        core_services.remove_user_from_area(area_id=user.current_area.id, user=user)

        force_user_disconect_by_company_and_user_id(
            company_id=company.id, user_id=user.id
        )

        result.append(user.id)

    return result


@shared_task
def launch_heartbeat_checkers():
    logger.info("check_company_areas")

    # TODO: This should be more specific query

    for company in Company.objects.all():
        check_company_areas.delay(company.id)
