# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = area_item_from_dict(json.loads(json_string))
import datetime
import logging
from dataclasses import dataclass
from typing import Optional, Any, TypeVar, Type, cast


logger = logging.getLogger(__name__)

T = TypeVar("T")

ISO_FORMAT = "%Y-%m-%d %H:%M:%S"


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_datetime(x: Any, nullable=True) -> str:
    if nullable and x is None:
        return None

    assert isinstance(x, datetime.datetime)
    return x.strftime(ISO_FORMAT)


def from_str_to_datetime(x: str) -> datetime.datetime:
    assert isinstance(x, str)

    return datetime.datetime.strptime(x, ISO_FORMAT)


@dataclass
class AreaItem:
    id: int
    x: int
    y: int
    name: str
    last_name: str
    status: str
    position: str
    avatar: str
    room: str
    is_online: bool
    last_seen: datetime.datetime
    jid: str

    @staticmethod
    def zero() -> 'AreaItem':
        return AreaItem(
            id=0,
            name="",
            last_name="",
            status={},
            position="",
            avatar="",
            room="",
            is_online=False,
            last_seen=None,
            x=0,
            y=0,
            jid=""
        )

    @staticmethod
    def from_dict(obj: Any) -> 'AreaItem':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        x = from_int(obj.get("x"))
        y = from_int(obj.get("y"))
        name = from_str(obj.get("name"))
        last_name = from_str(obj.get("last_name"))
        status = obj.get("status")
        position = from_str(obj.get("position"))
        avatar = from_str(obj.get("avatar"))
        room = from_str(obj.get("room"))
        is_online = from_bool(obj.get("is_online"))
        last_seen = (
            from_str_to_datetime(obj.get("last_seen"))
            if obj.get("last_seen")
            else None
        )
        jid = from_str(obj.get("jid"))

        return AreaItem(
            id=id,
            name=name,
            last_name=last_name,
            status=status,
            position=position,
            avatar=avatar,
            room=room,
            is_online=is_online,
            last_seen=last_seen,
            x=x,
            y=y,
            jid=jid
        )

    @staticmethod
    def from_user(User: Any, x: int, y: int, room: Optional[str]) -> dict:
        return AreaItem(
            id=User.id,
            name=User.name,
            last_name=User.last_name,
            status=User.current_status or {},
            position=User.position or "",
            avatar=User.avatar_thumb,
            room=room,
            is_online=True,
            last_seen=User.last_seen,
            x=x,
            y=y,
            jid=User.jid
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["x"] = from_int(self.x)
        result["y"] = from_int(self.y)
        result["name"] = from_str(self.name)
        result["last_name"] = from_str(self.last_name)
        result["status"] = self.status
        result["position"] = from_str(self.position)
        result["avatar"] = from_str(self.avatar)
        result["room"] = from_str(self.room)
        result["is_online"] = from_bool(self.is_online or True)
        result["last_seen"] = from_datetime(self.last_seen)
        result["jid"] = from_str(self.jid)
        return result


def area_item_from_dict(s: Any) -> AreaItem:
    return AreaItem.from_dict(s)


def area_item_to_dict(x: AreaItem) -> Any:
    return to_class(AreaItem, x)
