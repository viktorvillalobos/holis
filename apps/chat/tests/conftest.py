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


@pytest.fixture
def expected_chat_upload_file_fields():
    return {
        "id",
        "company_id",
        "message_uuid",
        "room_uuid",
        "user_id",
        "user_name",
        "attachment_url",
        "attachment_mimetype",
    }


@pytest.fixture
def expected_recent_fields():
    return {"name", "id", "room", "avatar_thumb"}


@pytest.fixture
def expected_message_raw_fields():
    return {"avatar_thumb", "user_name", "user_id", "user_name"}


@pytest.fixture
def expected_message_raw_with_attachments_fields():
    return {"avatar_thumb", "user_name", "user_id", "user_name", "attachments"}


@pytest.fixture
def expected_message_attachment_fields():
    return {
        "id",
        "company_id",
        "room_uuid",
        "user_id",
        "user_name",
        "attachment_url",
        "attachment_mimetype",
    }
