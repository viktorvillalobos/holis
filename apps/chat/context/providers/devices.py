from typing import Any, Iterable, Optional

import logging
from datetime import datetime
from fcm_django.models import FCMDevice
from uuid import UUID

logger = logging.getLogger(__name__)


def send_message_to_devices_by_user_ids(
    company_id: int, user_ids: Iterable[int], serialized_message: dict[str, Any]
) -> None:
    devices = FCMDevice.objects.filter(
        user_id__in=user_ids, user__company_id=company_id
    )
    devices.send_message({"type": "chat.fcm.message", **serialized_message})

    logger.info(f"Sending mesage to users ids: {user_ids}")
