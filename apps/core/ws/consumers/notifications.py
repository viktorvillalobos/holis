from typing import Dict

import logging

logger = logging.getLogger(__name__)


class NotificationMixin:
    async def notification(self, message: Dict) -> None:
        logger.info(message)
        await self.send_json(message)
