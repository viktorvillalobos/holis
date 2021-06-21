from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

import json
import pytest
from model_bakery import baker

from ..api import views as users_views
from . import baker_recipes as users_recipes


@pytest.mark.django_db
class TestUsersViewSet:
    def setup_method(self):
        self.user = users_recipes.user_viktor.make()
        self.users = baker.make(
            "users.User", company_id=self.user.company_id, _quantity=3
        )
        self.rf = APIRequestFactory()

    def test_list(self, expected_users_fields):
        url = reverse("api-v1:users:user-list")
        request = self.rf.get(url)

        force_authenticate(request, user=self.user)

        view = users_views.UserViewSet.as_view({"get": "list"})
        response = view(request).render()

        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)

        response_users_ids = {user["id"] for user in response_data["results"]}

        users_ids = {user.id for user in self.users}

        assert all(user_id in response_users_ids for user_id in users_ids)

        assert all(
            field in response_data["results"][0] for field in expected_users_fields
        )

        assert len(response_data["results"]) == 3

    def test_list_with_query_parameters(self, expected_users_fields):
        url = reverse("api-v1:users:user-list")
        request = self.rf.get(url, {"include_myself": True})

        force_authenticate(request, user=self.user)

        view = users_views.UserViewSet.as_view({"get": "list"})
        response = view(request).render()

        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.content)

        response_users_ids = {user["id"] for user in response_data["results"]}

        self.users.append(self.user)

        users_ids = {user.id for user in self.users}

        assert all(user_id in response_users_ids for user_id in users_ids)
        assert all(
            field in response_data["results"][0] for field in expected_users_fields
        )

        assert len(response_data["results"]) == 3
