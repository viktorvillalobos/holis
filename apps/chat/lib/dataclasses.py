from typing import Union

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class RecentRoomInfo:
    uuid: Union[UUID, str]
    image: str
    is_one_to_one: bool
    to_user_id: int
    to_user_name: str
    last_message_text: str
    last_message_ts: datetime
    last_message_user_id: int
    have_unread_messages: bool
