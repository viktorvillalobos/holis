from dataclasses import dataclass
from apps.chat import models as chat_models
from apps.users import models as user_models


@dataclass
class Message:
    room: chat_models.Room
    user: user_models.User
    text: str


class CreateMessage(Message):
    def execute(self):
        self.message = chat_models.Message.objects.create(
            room=self.room, user=self.user, text=self.str
        )
        return self

    def get_message(self):
        if not self.message:
            raise Exception('UC Must be executed before get message')

        return self.message
