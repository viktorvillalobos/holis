from django.db import IntegrityError
from django.db.models import QuerySet
from django.utils import timezone

import pytest
from datetime import date, datetime
from freezegun import freeze_time
from unittest import mock

from apps.core.tests import baker_recipes as core_recipes
from apps.users.lib.exceptions import UserDoesNotExist

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


@pytest.mark.django_db
class TestUpdateUserProfile:
    def setup_method(self):
        self.user = user_recipes.user_viktor.make()

    def test_update_user_profile(self, django_assert_num_queries):

        expected_kwargs = dict(
            id=self.user.id,
            company_id=self.user.company_id,
            birthday=date(1991, 2, 15),
            email="other@email.com",
            name="Linus Torvalds",
            position="Linux Creator",
        )

        with django_assert_num_queries(num=1):
            user_providers.update_user_profile(**expected_kwargs)

        self.user.refresh_from_db()

        for key, value in expected_kwargs.items():
            assert getattr(self.user, key) == value

    def test_not_existent_user_raise_exception(self):
        kwargs = dict(
            id=-999,
            company_id=-999,
            birthday=date(1991, 2, 15),
            email="other@email.com",
            name="Linus Torvalds",
            position="Linux Creator",
        )

        with pytest.raises(UserDoesNotExist):
            user_providers.update_user_profile(**kwargs)


@pytest.mark.django_db
def test_get_users_by_ids(django_assert_num_queries):
    user1 = user_recipes.user_julls.make()
    user2 = user_recipes.user_viktor.make()

    with django_assert_num_queries(num=0):
        result = user_providers.get_users_by_ids(
            company_id=user1.company_id, users_ids={user1.id, user2.id}
        )

    assert isinstance(result, QuerySet)

    with django_assert_num_queries(num=1):
        result = list(result)

    assert result == [user1, user2]
