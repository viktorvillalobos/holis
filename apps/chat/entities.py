from dataclasses import dataclass

from apps.chat import models as chat_models
from apps.users import models as user_models


@dataclass
class Message:
    room: chat_models.Room
    user: user_models.User
    text: str
