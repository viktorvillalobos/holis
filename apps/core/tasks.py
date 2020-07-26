import datetime as dt
from django.utils import timezone
from celery import shared_task
from celery.utils.log import get_task_logger
from apps.core.models import Company
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

logger = get_task_logger(__name__)


@shared_task
def check_company_areas(company_id: str) -> None:
    company = Company.objects.get(id=company_id)
    logger.info('check_company_areas')

    result = []
    for user in company.users.filter(
        last_seen__lt=timezone.now() - dt.timedelta(seconds=60)
    ):
        async_to_sync(channel_layer.group_send)(
            f"company-{company.id}", {"type": "force.disconnect", "user_id": user.id}
        )
        result.append(user.id)

    return result


@shared_task
def launch_heartbeat_checkers():
    logger.info('check_company_areas')
    for company in Company.objects.all():
        check_company_areas.delay(company.id)
