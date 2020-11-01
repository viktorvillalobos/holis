import pytest
from model_bakery import baker


@pytest.fixture
def company():
    return baker.make("core.Company")


@pytest.fixture
def user(company):
    return baker.make("users.User", company=company)


@pytest.fixture
def user2(company):
    return baker.make("users.User", company=company)


@pytest.fixture
def one_to_one_room(user, user2):
    return baker.make(
        "room", is_one_to_one=True, company=user.company, members=[user, user2]
    )