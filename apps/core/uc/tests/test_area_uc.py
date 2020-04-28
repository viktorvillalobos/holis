from typing import Dict, List
import pytest

from apps.core.uc.area_uc import GetStateAreaUC
from apps.core.tests.factories import AreaFactory


class TestGetUsersAreaUC:
    def test_execute(self) -> None:
        item: Dict = {
            "id": 1,
            "name": "Victor",
            "last_name": "Villalobos",
            "status": "Coding",
            "position": "FullStack Developer",
            "is_online": True,
            "x": 0,
            "y": 1,
        }

        expected_results: List = [item for x in range(10)]

        area = AreaFactory.build()
        instance = GetStateAreaUC(area)
        assert instance.execute() == expected_results
