from typing import Any, Dict

from channels.generic.websocket import JsonWebSocketConsumer


class ProjectConsumer(JsonWebSocketConsumer):
    async def receive_json(self, message: Dict[str, Any]) -> Dict[str, Any]:
        self.send_json({"type": "project.task.create"})

        _msg = "type not handled by GridConsumer"
        await self.send_json({"error": _msg})
