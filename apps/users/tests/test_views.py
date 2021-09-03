from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

import json
import pytest
from dataclasses import asdict
from model_bakery import baker
from unittest import mock
from uuid import uuid4

from ..api.v100 import views as users_views
from ..context.models import User
from ..lib.dataclasses import UserInvitationData
from . import baker_recipes as users_recipes


@pytest.mark.skip("We need to figure it out how to solve this problem")
class TestUsersViewSet:
    def setup_method(self):
        statuses = mock.Mock()
        statuses.all.return_value = []

        self.users = []
        for x in range(3):
            self.users.append(
                User(
                    company_id=1,
                    avatar="https://demo_avatar.png",
                    # statuses=statuses
                )
            )

        self.user = self.users[0]
        self.rf = APIRequestFactory()

    def test_list(self, expected_users_fields, mocker):
        mocked_provider = mocker.patch(
            "apps.users.api.views.users_providers.get_users_with_statuses"
        )
        mocked_provider.return_value = self.users

        url = reverse("api-v1:users:user-list")
        request = self.rf.get(url)
        request.company_id = 1

        force_authenticate(request, user=self.user)

        view = users_views.UserViewSet.as_view({"get": "list"})
        response = view(request).render()

        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)

        response_users_ids = {user["id"] for user in response_data["results"]}

        users_ids = {user.id for user in self.users}

        mocked_provider.assert_called_once_with(
            company_id=1, user_id=self.user.id, include_myself=False, name=None
        )

        assert all(user_id in response_users_ids for user_id in users_ids)

        assert all(
            field in response_data["results"][0] for field in expected_users_fields
        )

        assert len(response_data["results"]) == 3

    def test_list_with_query_parameters(self, expected_users_fields, mocker):
        mocked_provider = mocker.patch(
            "apps.users.api.views.users_providers.get_users_with_statuses"
        )
        mocked_provider.return_value = self.users

        url = reverse("api-v1:users:user-list")
        request = self.rf.get(url, {"include_myself": True, "name": "Viktor"})
        request.company_id = 1

        force_authenticate(request, user=self.user)

        view = users_views.UserViewSet.as_view({"get": "list"})
        response = view(request).render()

        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)

        response_users_ids = {user["id"] for user in response_data["results"]}

        users_ids = {user.id for user in self.users}

        mocked_provider.assert_called_once_with(
            company_id=1, user_id=self.user.id, include_myself=True, name="Viktor"
        )


class TestUserInvitationViewSet:
    def setup_method(self):
        self.rf = APIRequestFactory()
        self.url = reverse("api-v1:users:invitate")
        self.user = User(
            id=1,
            company_id=1,
            avatar="https://demo_avatar.png",
            # statuses=statuses
        )
        self.company_id = 1

    @mock.patch("apps.users.api.v100.views.user_tasks.send_users_invitations")
    @mock.patch("apps.users.api.v100.views.user_services.create_users_invitations")
    def test_user_invitation_create_success(
        self, mocked_create_users_invitations, mocked_send_users_invitations
    ):
        invitation1 = UserInvitationData(uuid=uuid4(), email="john@doe.com")
        invitation2 = UserInvitationData(uuid=uuid4(), email="doe@john.com")

        mocked_create_users_invitations.return_value = [invitation1, invitation2]

        data = {"emails": [invitation1.email, invitation2.email]}

        request = self.rf.post(self.url, data)
        request.company_id = self.company_id

        force_authenticate(request, user=self.user)

        view = users_views.UserInvitationViewSet.as_view({"post": "create"})
        response = view(request).render()

        assert response.status_code == status.HTTP_200_OK

        mocked_create_users_invitations.assert_called_once_with(
            company_id=self.company_id,
            user_id=self.user.id,
            emails=[invitation1.email, invitation2.email],
        )

        invitation_values = [asdict(invitation1), asdict(invitation2)]

        mocked_send_users_invitations.delay.assert_called_once_with(invitation_values)

    def test_create_user_with_bad_formed_emails_fails(self):

        data = {"emails": ["john@doe.com", "BAD-EMAIL"]}
        request = self.rf.post(self.url, data)
        request.company_id = self.company_id

        force_authenticate(request, user=self.user)

        view = users_views.UserInvitationViewSet.as_view({"post": "create"})
        response = view(request).render()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
