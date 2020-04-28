"""
    UseCases for Area
"""
from typing import Dict, List
from apps.core.uc.abstracts import AbstractModelUC


class GetUsersAreaUC(AbstractModelUC):
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

    def execute(self) -> List[Dict]:

        item: Dict = {
            "name": "Victor",
            "last_name": "Villalobos",
            "status": "Coding",
            "position": "FullStack Developer",
            "is_online": True,
            "x": 0,
            "y": 1
        }
        return [item for x in range(10)]
