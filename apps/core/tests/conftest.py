import pytest
from model_bakery import baker


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
def active_user(company):
    return baker.make("users.User", company=company, name="John Doe")


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
