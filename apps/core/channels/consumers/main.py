from typing import Dict

from django.conf import settings
from django.utils.translation import ugettext as _

import logging
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from apps.users.services import serialize_user

from . import grid as grid_handlers

logger = logging.getLogger(__name__)

COMPANY_MAIN_CHANNEL = "company-{}"


class MainConsumer(AsyncJsonWebsocketConsumer):
    @property
    def company_channel(self):
        company_id = self.scope["user"].company_id
        return COMPANY_MAIN_CHANNEL.format(company_id)

    async def get_groups(self):
        return [self.company_channel]

    async def send_me_data(self):
        serialized_user = await database_sync_to_async(serialize_user)(
            self.scope["user"]
        )

        if self.scope["user"].id:
            await self.send_json({"type": "me.data", "user": serialized_user})

    async def connect_to_groups(self):
        for group in await self.get_groups():
            await self.channel_layer.group_add(group, self.channel_name)

    async def receive_json(self, message):
        """
        This method receive jsons for clients, and
        distribute in diferent methods
        """

        try:
            _type = message["type"]
        except KeyError:
            _type = "error"
            _msg = _("Type is required")

        user = self.scope["user"]

        if _type == "error":
            return await self.send_json({"error": _msg})

        elif _type == "grid.position":
            await grid_handlers.handle_grid_position(
                channel_layer=self.channel_layer,
                company_channel=self.company_channel,
                user=user,
                message=message,
            )
        elif _type == "grid.clear":
            await grid_handlers.handle_clear_user_position(
                channel_layer=self.channel_layer,
                company_channel=self.company_channel,
                user=user,
            )

        elif _type == "grid.status":
            await grid_handlers(
                channel_layer=self.channel_layer,
                company_channel=self.company_channel,
                user=user,
                message=message,
            )

        elif _type == "grid.heartbeat":
            await grid_handlers.execute_heartbeat(user=self.scope["user"])

        elif _type == "grid.force.disconnect":
            await grid_handlers.handle_force_disconnect(
                channel_layer=self.channel_layer,
                company_channel=self.company_channel,
                message=message,
            )
        else:
            _msg = _("type not handled by GridConsumer")
            return await self.send_json({"error": _msg})

    async def connect(self):
        # Join room group
        if self.scope["user"].is_authenticated:
            await self.connect_to_groups()
            await self.accept()

    async def disconnect(self, close_code):
        logger.info("MainConsumer.disconnect")
        await grid_handlers.handle_clear_user_position(
            channel_layer=self.channel_layer,
            company_channel=self.company_channel,
            user=self.scope["user"],
        )

        for group in self.groups:
            await self.channel_layer.group_discard(group, self.channel_name)

    async def grid_position(self, message):
        await self.send_json(message)

    async def grid_disconnect(self, message):
        await self.send_json(message)

    async def grid_status(self, message):
        await self.send_json(message)
