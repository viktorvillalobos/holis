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
