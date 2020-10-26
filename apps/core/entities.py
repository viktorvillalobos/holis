from dataclasses import dataclass
from typing import Dict

from .models import Area as AreaModel


@dataclass
class Area:
    id: int
    company: int
    name: str
    parent: int
    width: int
    height: int
    state: Dict

    @classmethod
    def load_from_model(cls, area: AreaModel) -> AreaModel:
        return cls(
            id=area.id,
            company=area.company_id,
            name=area.name,
            parent=area.parent_id,
            width=area.width,
            height=area.height,
            state=area.state,
        )


@dataclass
class Point:
    x: int
    y: int
