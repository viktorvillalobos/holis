from django.db import IntegrityError
from django.utils import timezone

import datetime
import pytest
from freezegun import freeze_time

from apps.core.tests import baker_recipes as core_recipes

from ...context.models import User
from ...context.providers import user as user_providers
from .. import baker_recipes as user_recipes


@freeze_time("1992-02-14 00:00:00", tz_offset=-4)
@pytest.mark.django_db
def test_touch_user_by_user_and_area_id():
    area = core_recipes.default_area.make()
    user_without_area = user_recipes.user_viktor.make(current_area=None)
    user_providers.touch_user_by_user_and_area_id(
        user_id=user_without_area.id, area_id=area.id
    )

    user = User.objects.get(id=user_without_area.id)

    assert user.current_area_id == area.id
    assert user.last_seen == timezone.now()


@freeze_time("1992-02-14 00:00:00", tz_offset=-4)
@pytest.mark.django_db
def test_disconnect_user_by_id():
    area = core_recipes.default_area.make()
    user_without_area = user_recipes.user_viktor.make(current_area=None)

    # We set the area and last_seen
    user_providers.touch_user_by_user_and_area_id(
        user_id=user_without_area.id, area_id=area.id
    )

    user = user_providers.get_user_by_id(user_id=user_without_area.id)

    assert user.current_area_id == area.id
    assert user.last_seen == timezone.now()

    # We disconnect the user
    user_providers.disconnect_user_by_id(user_id=user.id)

    user = user_providers.get_user_by_id(user_id=user.id)

    assert user.current_area is None
    assert user.last_seen is None


@pytest.mark.django_db(transaction=True)
def test_touch_user_by_user_and_area_id_with_incorrect_area_raise_foreign_key_constraint_exception():
    nonexistent_area_id = 999
    user_without_area = user_recipes.user_viktor.make(current_area=None)

    with pytest.raises(IntegrityError):
        user_providers.touch_user_by_user_and_area_id(
            user_id=user_without_area.id, area_id=nonexistent_area_id
        )
