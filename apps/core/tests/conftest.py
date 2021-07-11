import pytest
from channels.db import database_sync_to_async
from model_bakery import baker

from apps.users.tests import baker_recipes as user_recipes

from . import baker_recipes as core_recipes


@pytest.fixture
def company():
    return baker.make("core.Company", name="EvilCorp")


@pytest.fixture
def area(company):
    return baker.make("core.Area", company=company, width=60, height=60)


@pytest.fixture
def announcement(company):
    return baker.make("core.Announcement", company=company)


@pytest.fixture
def changelog(company):
    return baker.make("core.Changelog", company=company)


@pytest.fixture
def cached_position_fields():
    return {
        "id",
        "x",
        "y",
        "name",
        "last_name",
        "status",
        "position",
        "avatar",
        "room",
        "is_online",
        "last_seen",
        "jid",
        "area_id",
    }


@pytest.fixture
def create_status_test_data():
    @database_sync_to_async
    def _create_status_test_data():
        user = user_recipes.user_julls.make()
        area = core_recipes.default_area.make(company_id=user.company_id)
        return user, area

    return _create_status_test_data
