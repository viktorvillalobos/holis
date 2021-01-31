# core/ws/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/grid/", consumers.MainConsumer.as_asgi()),
    path("ws/notifications/", consumers.NotificationsConsumer.as_asgi()),
]
