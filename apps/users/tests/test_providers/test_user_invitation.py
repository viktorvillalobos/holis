import pytest

from ...context.providers import user_invitation as user_invitation_providers
from .. import baker_recipes as user_recipes


@pytest.mark.django_db
def test_create_users_invitations():
    user = user_recipes.user_joel.make()

    email1 = "seba@soy.pelon"
    email2 = "tatan@soy.tu"

    users = user_invitation_providers.create_users_invitations(
        company_id=user.company_id, user_id=user.id, emails=[email1, email2]
    )

    user_1, user_2 = users
    assert user_1.email == email1
    assert user_2.email == email2
