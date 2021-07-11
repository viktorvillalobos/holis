from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

import json
import pytest
from model_bakery import baker
from unittest import mock

from ..api.v100 import views as users_views
from ..context.models import User
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
