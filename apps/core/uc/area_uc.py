"""
    UseCases for Area
"""
import logging
from typing import Dict, List, Tuple

import numpy as np
from apps.core.uc.abstracts import AbstractModelUC
from apps.users.models import User

logger = logging.getLogger(__name__)


class BaseAreaUC(AbstractModelUC):
    """
        Allow to handle the state of area
        Area.state contains the status of the area,
        the users inside an area

        state is an two dimensions array
        to handle the frontend HexGrid


        1 0 0 0 0 0 0 0 0 0
        0 1 0 0 0 0 0 0 0 0
        0 0 1 0 0 0 0 0 0 0
        0 0 0 1 0 0 0 0 0 0
        0 0 0 0 1 0 0 0 0 0
        0 0 0 0 0 1 0 0 0 0
        0 0 0 0 0 0 1 0 0 0
        0 0 0 0 0 0 0 1 0 0
        0 0 0 0 0 0 0 0 1 0
        0 0 0 0 0 0 0 0 0 1

        All 1 are an users.

    """

    def __init__(self, instance) -> None:
        self.instance = instance
        created, self.state = self.get_or_create_state()
        if created:
            self.save_state()

    dtype = [
        ('id', np.int32),
        ('name', (np.str_, 100)),
        ('last_name', (np.str_, 100)),
        ('status', (np.str_, 100)),
        ('position', (np.str_, 100)),
        ('avatar', (np.str_, 255)),
        ('room', (np.str_, 255)),
        ('is_online', np.bool_),
    ]

    def convert_to_tuple(self, _list: List) -> List[List[Tuple]]:
        # TODO: Esto no deberia ser obligatorio, no entiendo porque
        # es ineficiente, cambiar urgente.
        result = []
        for x in _list:
            sublist = []
            for y in x:
                sublist.append(tuple(y))
            result.append(sublist)
        return result

    def get_or_create_state(self) -> Tuple[bool, np.ndarray]:
        if not self.instance.state:
            return (
                True,
                np.zeros(
                    (self.instance.width, self.instance.height),
                    dtype=self.dtype,
                ),
            )

        if len(self.instance.state[0][0]) != len(self.dtype):
            logger.info("Converting to new dtype")
            # TODO: Convert changes, handle migrations
            # in dtype for now we recreate the area
            return (
                True,
                np.zeros(
                    (self.instance.width, self.instance.height),
                    dtype=self.dtype,
                ),
            )

        converted = self.convert_to_tuple(self.instance.state)
        return False, np.array(converted, dtype=self.dtype)

    def save_state(self):
        self.instance.state = self.state.tolist()
        self.instance.save()

    @property
    def connected_idxs(self):
        return np.argwhere(self.state["id"] != 0)

    def get_serialized_connected(self):
        serialized = []
        for x, y in self.connected_idxs:
            item = {}
            item["id"] = int(self.state[x, y][0])
            item["name"] = self.state[x, y][1]
            item["last_name"] = self.state[x, y][2]
            item["status"] = self.state[x, y][3]
            item["position"] = self.state[x, y][4]
            item["avatar"] = self.state[x, y][5]
            item["room"] = self.state[x, y][6]
            item["is_online"] = True
            item["x"] = int(x)
            item["y"] = int(y)
            serialized.append(item)

        return serialized

    def get_record_from_user(self, user: User, x: int, y: int, room: str) -> Tuple:
        return (
            user.id,
            user.name,
            user.last_name,
            user.current_status,
            user.position,
            user.avatar_thumb,
            room,
            True,
        )

    def get_empty_record(self):
        return (0, '', '', '', '', '', '', False)

    def get_user_position(self, user: User):
        return np.argwhere(self.state["id"] == user.id)

    def clear_current_user_position(self, user: User):
        logger.info("clear_current_user_position")
        try:
            x, y = self.get_user_position(user)[0]
        except IndexError:
            return None
        else:
            self.state[x, y] = self.get_empty_record()
            self.save_state()
            return int(x), int(y)


class GetStateAreaUC(BaseAreaUC):
    def execute(self) -> List[Dict]:
        return self.get_serialized_connected()


class SaveStateAreaUC(BaseAreaUC):
    """
        Save the position of person inside the state
    """

    def execute(self, user: User, x: int, y: int, room: str) -> List:
        positions = self.clear_current_user_position(user)
        self.state[x, y] = self.get_record_from_user(user, x, y, room)
        self.save_state()
        return positions


class ClearStateAreaUC(BaseAreaUC):
    """
        Clear the person when disconnect
    """

    def execute(self, user: User):
        self.clear_current_user_position(user)
