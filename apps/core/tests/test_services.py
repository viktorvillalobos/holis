from django.conf import settings

import pytest

from .. import services as core_services
from ..lib.dataclasses import AreaItem, PointData
from ..models import Area


@pytest.mark.django_db
def test_get_area(area) -> None:
    area_entity = core_services.get_area(area.pk)

    assert area.id == area_entity.id
    assert area.name == area_entity.name


@pytest.mark.django_db
def test_get_area_items_for_connected_users_by_id(
    area: Area, user: settings.AUTH_USER_MODEL
) -> None:
    expected_result = []
    state = core_services.get_area_items_for_connected_users_by_id(area_id=area.id)

    assert isinstance(state, list)
    assert state == expected_result


@pytest.mark.django_db
def test_move_user_to_point_in_area_state_by_area_user_and_room(
    area: Area, active_user: settings.AUTH_USER_MODEL
) -> None:

    asked_point = PointData(20, 20)
    core_services.move_user_to_point_in_area_state_by_area_user_and_room(
        area_id=area.pk, user=active_user, to_point_data=asked_point, room="EvilCorp"
    )
    state = core_services.get_area_items_for_connected_users_by_id(area_id=area.id)

    assert isinstance(state, list)
    assert len(state) == 1
    assert isinstance(state[0], dict)

    area_item = AreaItem.from_dict(state[0])

    assert area_item.name == "John Doe"


@pytest.mark.django_db
def test_remove_user_from_area_by_area_and_user_id(
    area: Area, active_user: settings.AUTH_USER_MODEL
) -> None:
    asked_point = PointData(20, 20)
    core_services.move_user_to_point_in_area_state_by_area_user_and_room(
        area_id=area.pk, user=active_user, to_point_data=asked_point, room="EvilCorp"
    )
    state = core_services.get_area_items_for_connected_users_by_id(area_id=area.id)

    assert isinstance(state, list)
    assert len(state) == 1
    assert isinstance(state[0], dict)

    area_item = AreaItem.from_dict(state[0])

    assert area_item.name == "John Doe"

    core_services.remove_user_from_area_by_area_and_user_id(
        area_id=area.id, user=active_user
    )
    state = core_services.get_area_items_for_connected_users_by_id(area_id=area.id)

    assert len(state) == 0
