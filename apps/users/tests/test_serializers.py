from django.contrib.auth import get_user_model

import pytest

from ..api.serializers import serialize_user_queryset
from .baker_recipes import user_viktor

User = get_user_model()


@pytest.mark.django_db
def test_serialize_queryzet_contract():
    user = user_viktor.make()
    queryset = User.objects.all()

    serialized = serialize_user_queryset(queryset)

    assert isinstance(serialized["results"], list)
    assert serialized["results"][0]["id"] == user.id
