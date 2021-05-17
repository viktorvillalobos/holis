from django.core.cache import cache

import pytest
from model_bakery import baker

from apps.users.lib.constants import USER_STATUS_KEY

from ...models import Status
from ...providers import status as status_providers
from .. import baker_recipes as user_recipes


@pytest.mark.django_db
def test_get_user_statuses_by_user_id():
    status = user_recipes.user_status_holidays.make()
    results = list(
        status_providers.get_user_statuses_by_user_id(
            company_id=status.user.company_id, user_id=status.user_id
        )
    )

    assert Status.objects.count() == 1
    assert results[0] == status


@pytest.mark.django_db
def test_inactivate_all_user_status_by_user_id():
    user = user_recipes.user_viktor.make()
    status = baker.make("users.Status", is_active=True, user=user, _quantity=3)

    status_providers.inactivate_all_user_status_by_user_id(
        company_id=user.company_id, user_id=user.id
    )

    statuses = Status.objects.filter(user_id=user.id)
    assert any(status.is_active for status in statuses)


@pytest.mark.django_db
class TestUserStatusSet:
    def setup_method(self, method):
        self.user = user_recipes.user_viktor.make()
        self.statuses = baker.make(
            "users.Status",
            is_active=False,
            company_id=self.user.company_id,
            user=self.user,
            _quantity=3,
        )

    def test_set_active_status_by_user_and_status_id(self):
        to_active_status = self.statuses[0]

        status_providers.set_active_status_by_user_and_status_id(
            company_id=self.user.company_id,
            user_id=self.user.id,
            status_id=to_active_status.id,
        )

        cached_status = cache.get(
            USER_STATUS_KEY.format(self.user.company_id, self.user.id)
        )

        assert isinstance(cached_status, dict)
        assert cached_status["id"] == to_active_status.id
        assert cached_status["icon_text"] == to_active_status.icon_text
        assert cached_status["text"] == to_active_status.text

    def test_get_user_active_status_from_cache_by_user_id(self):
        to_active_status = self.statuses[0]

        status_providers.set_active_status_by_user_and_status_id(
            company_id=self.user.company_id,
            user_id=self.user.id,
            status_id=to_active_status.id,
        )

        cached_status = status_providers.get_user_active_status_from_cache_by_user_id(
            company_id=to_active_status.user.company_id,
            user_id=to_active_status.user_id,
        )

        assert isinstance(cached_status, dict)
        assert cached_status["id"] == to_active_status.id
        assert cached_status["icon_text"] == to_active_status.icon_text
        assert cached_status["text"] == to_active_status.text
