import json
from typing import Dict
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer


logger = logging.getLogger(__name__)


class MainConsumer(AsyncJsonWebsocketConsumer):
    groups = ["adslab", "adslab_global"]

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def notify(self, message: Dict):
        await self.send_json(message)

    async def receive_json(self, content):
        logger.info(content)
        message: Dict = {"message": content["message"], "user": "Pitufin"}
        await self.notify(message)
