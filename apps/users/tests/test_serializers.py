from django.contrib.auth import get_user_model

import pytest

from ..api.serializers import serialize_user_queryset

User = get_user_model()


@pytest.mark.django_db
def test_serialize_queryzet_contract(active_user):
    queryset = User.objects.all()

    serialized = serialize_user_queryset(queryset)

    assert isinstance(serialized["results"], list)
    assert serialized["results"][0]["id"] == active_user.id
