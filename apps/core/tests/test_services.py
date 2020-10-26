import pytest
from django.conf import settings

from ..entities import Point
from ..models import Area
from ..services import add_user_to_area, get_area, get_area_state, remove_user_from_area
from ..uc.item import AreaItem


@pytest.mark.django_db
def test_get_area(area) -> None:
    area_entity = get_area(area.pk)

    assert area.id == area_entity.id
    assert area.name == area_entity.name


@pytest.mark.django_db
def test_get_area_state(area: Area, user: settings.AUTH_USER_MODEL) -> None:
    expected_result = []
    state = get_area_state(area.pk)

    assert isinstance(state, list)
    assert state == expected_result


@pytest.mark.django_db
def test_add_user_to_area(area: Area, active_user: settings.AUTH_USER_MODEL) -> None:

    asked_point = Point(20, 20)
    add_user_to_area(
        area_id=area.pk, user=active_user, point=asked_point, room="EvilCorp"
    )
    state = get_area_state(area.pk)

    assert isinstance(state, list)
    assert len(state) == 1
    assert isinstance(state[0], dict)

    area_item = AreaItem.from_dict(state[0])

    assert area_item.name == "John Doe"


@pytest.mark.django_db
def test_remove_user_from_area(
    area: Area, active_user: settings.AUTH_USER_MODEL
) -> None:
    asked_point = Point(20, 20)
    add_user_to_area(
        area_id=area.pk, user=active_user, point=asked_point, room="EvilCorp"
    )
    state = get_area_state(area.pk)

    assert isinstance(state, list)
    assert len(state) == 1
    assert isinstance(state[0], dict)

    area_item = AreaItem.from_dict(state[0])

    assert area_item.name == "John Doe"

    remove_user_from_area(area.pk, active_user)
    state = get_area_state(area.pk)

    assert len(state) == 0
