import datetime as dt

from asgiref.sync import async_to_sync
from celery import shared_task
from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer
from django.db.models import Q
from django.utils import timezone

from apps.core.models import Company
from apps.core.uc.area_uc import ClearStateAreaUC
from apps.users.models import User

channel_layer = get_channel_layer()

logger = get_task_logger(__name__)


@shared_task
def check_company_areas(company_id: str) -> None:
    company = Company.objects.get(id=company_id)
    logger.info("check_company_areas")

    result = []
    query = (
        User.objects.filter(company=company)
        .filter(last_seen__lt=timezone.now() - dt.timedelta(seconds=60))
        .exclude(Q(last_seen=None) | Q(current_area=None))
    )

    for user in query:
        async_to_sync(channel_layer.group_send)(
            f"company-{company.id}", {"type": "force.disconnect", "user_id": user.id}
        )
        result.append(user.id)

        uc = ClearStateAreaUC(user.current_area)
        uc.execute(user)

    return result


@shared_task
def launch_heartbeat_checkers():
    logger.info("check_company_areas")
    for company in Company.objects.all():
        check_company_areas.delay(company.id)
