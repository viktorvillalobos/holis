from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


def send_notification(group: str, ntype: str, message: str) -> None:
    payload = {"type": "notification", "ntype": ntype, "message": message}
    async_to_sync(channel_layer.group_send)(group, payload)
