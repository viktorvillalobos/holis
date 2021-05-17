from django.conf import settings
from django.utils import timezone

import pytest
from freezegun import freeze_time

from apps.users.tests import baker_recipes as user_recipes

from .. import services as core_services
from ..lib.dataclasses import AreaItem, PointData
from ..models import Area
from . import baker_recipes as core_recipes


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
        area_id=area.id, user_id=active_user.id
    )
    state = core_services.get_area_items_for_connected_users_by_id(area_id=area.id)

    assert len(state) == 0


@pytest.mark.django_db
@freeze_time("1992-02-14 00:00:00", tz_offset=-4)
class TestCachedPosition:
    def setup_method(self, method):
        self.user = user_recipes.user_viktor.make()
        self.area = core_recipes.default_area.make(company_id=self.user.company_id)
        self.expected_datetime_string = timezone.now().isoformat()

        core_services.set_cached_position(
            company_id=self.user.company_id,
            area=self.area.id,
            user=self.user,
            x=10,
            y=15,
            room="custom-room",
        )

    def test_get_cached_position(self, cached_position_fields):
        cached_position = core_services.get_cached_position(
            company_id=self.user.company_id, user_id=self.user.id
        )

        assert isinstance(cached_position, dict)
        assert all(
            field_name in cached_position for field_name in cached_position_fields
        )
        assert cached_position["id"] == self.user.id
        assert cached_position["x"] == 10
        assert cached_position["y"] == 15
        assert cached_position["room"] == "custom-room"
        assert cached_position["name"] == self.user.name
        assert cached_position["last_name"] == self.user.last_name
        assert cached_position["position"] == self.user.position
        assert cached_position["area_id"] == self.area.id
        assert cached_position["jid"] == self.user.jid
        assert cached_position["avatar"] == self.user.avatar.url
        assert cached_position["last_seen"] == self.expected_datetime_string

    def test_delete_cached_position(self):
        cached_position = core_services.get_cached_position(
            company_id=self.user.company_id, user_id=self.user.id
        )

        assert isinstance(cached_position, dict)

        core_services.delete_cached_position(
            company_id=self.user.company_id, user_id=self.user.id
        )

        assert (
            core_services.get_cached_position(
                company_id=self.user.company_id, user_id=self.user.id
            )
            == None
        )
