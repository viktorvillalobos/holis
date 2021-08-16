import datetime as dt
from dataclasses import dataclass

from ..context.models import User as UserModel


@dataclass
class UserData:
    id: int
    name: str
    company: int
    position: str
    default_area: int
    current_area: int
    birthday: dt.date
    avatar = str
    last_seen = dt.datetime

    @classmethod
    def load_from_model(cls, instance: UserModel):
        return cls(
            id=instance.id,
            name=instance.name,
            company=instance.company_pk,
            position=instance.position,
            default_area=instance.default_area_pk,
            current_area=instance.current_area_pk,
            birthday=instance.birthday,
            avatar=instance.avatar.url,
            last_seen=instance.last_seen,
        )


@dataclass
class StatusCachedData:
    """
    This represents the data thats comes from Redis
    """

    id: int
    icon_text: str
    text: str
