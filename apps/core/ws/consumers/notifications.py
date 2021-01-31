from typing import Dict

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from apps.users import services as user_services

import logging

logger = logging.getLogger(__name__)


class NotificationsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Join room group
        user = self.scope["user"]

        if not user.is_authenticated:
            return

        user_notification_channel = (
            user_services.get_user_notification_channel_by_user_id(
                user_id=user.id,
            )
        )

        await self.channel_layer.group_add(
            user_notification_channel, self.channel_name
        )
        await self.accept()

    async def notification(self, message: Dict) -> None:
        logger.info(message)
        await self.send_json(message)
