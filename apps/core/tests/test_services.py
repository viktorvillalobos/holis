import pytest

from ..models import Area
from ..services import get_area_state


@pytest.mark.django_db
def test_get_area_state(area: Area) -> None:
    state = get_area_state(area)

    assert isinstance(state, list)
