# core/ws/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [path(r"", consumers.MainConsumer)]
