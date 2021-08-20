from typing import Optional, Union

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from apps.users.lib import dataclasses as users_dataclasses


@dataclass
class RecentRoomInfo:
    uuid: Union[UUID, str]
    name: str
    is_conversation: bool
    is_one_to_one: bool
    last_message_text: str
    last_message_ts: datetime
    last_message_user_id: int
    have_unread_messages: bool
    members_count: int
    to_user_id: Optional[int]  # Only if is a one_to_one
    image: Optional[str]


@dataclass
class RoomData:
    company_id: int
    uuid: Union[UUID, str]
    is_conversation: bool
    is_one_to_one: bool
    members: list[users_dataclasses.UserData]
    admins: list[users_dataclasses.UserData]
    subject: str
    name: str
    is_public: bool
    any_can_invite: bool
    is_one_to_one: bool
    max_users: int
    image_url: str
