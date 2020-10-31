# chat/ws/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [path("chat/<str:room_name>/", consumers.ChatConsumer)]