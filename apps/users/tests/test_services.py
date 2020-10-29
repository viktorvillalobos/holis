import pytest
from django.conf import settings

from ..services import serialize_user


@pytest.mark.django_db
def test_service_serialize_user(active_user: settings.AUTH_USER_MODEL) -> None:
    serialized_user = serialize_user(active_user)

    assert isinstance(serialized_user, dict)
