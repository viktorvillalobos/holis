from typing import Union

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class RecentChatInfo:
    room_uuid: Union[UUID, str]
    user_avatar_thumb: str
    user_id: int
    user_name: str
    message: str
    created: datetime
    have_unread_messages: bool
