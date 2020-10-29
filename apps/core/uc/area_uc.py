"""
    UseCases for Area
"""
import logging
from typing import Dict, List, Tuple

import numpy as np

from apps.users.models import User

from ..entities import AreaItem, Point
from ..models import Area
from .abstracts import AbstractModelUC

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
        assert isinstance(instance, Area)
        self.instance = instance
        created, self.state = self.get_or_create_state()
        if created:
            self.save_state()

    def get_or_create_state(self) -> Tuple[bool, np.ndarray]:
        if not self.instance.state:
            return (
                True,
                [
                    [AreaItem.zero() for x in range(self.instance.width)]
                    for x in range(self.instance.height)
                ],
            )

        return (
            False,
            [[AreaItem.from_dict(x) for x in row] for row in self.instance.state],
        )

    def save_state(self):
        self.instance.state = [[x.to_dict() for x in row] for row in self.state]
        self.instance.save()

    @property
    def connected_idxs(self) -> dict:
        logger.info("connected_idxs")
        result = []
        for row in self.state:
            result += [x for x in row if x.id != 0]

        return result

    def get_serialized_connected(self):
        return [x.to_dict() for x in self.connected_idxs]

    def get_empty_record(self):
        return AreaItem.zero()

    def get_user_position(self, user: User) -> dict:
        logger.info("get_user_position")
        x_pos = 0
        y_pos = 0

        for x, row in enumerate(self.state):
            for y, column in enumerate(row):
                if user.id == column.id:
                    x_pos = x
                    y_pos = y
                    break

        return Point(x=x_pos, y=y_pos)

    def clear_current_user_position(self, user: User):
        try:
            point = self.get_user_position(user)
        except IndexError:
            return None
        else:
            self.state[point.x][point.y] = self.get_empty_record()
            self.save_state()
            return point


class GetStateAreaUC(BaseAreaUC):
    def execute(self) -> List[Dict]:
        return self.get_serialized_connected()


class SaveStateAreaUC(BaseAreaUC):
    """
        Save the position of person inside the state
    """

    def execute(self, user: User, x: int, y: int, room: str) -> Point:
        old_point = self.clear_current_user_position(user)
        self.state[x][y] = AreaItem.from_user(user, x, y, room)
        self.save_state()
        return old_point


class ClearStateAreaUC(BaseAreaUC):
    """
        Clear the person when disconnect
    """

    def execute(self, user: User):
        user.disconnect()
        self.clear_current_user_position(user)
