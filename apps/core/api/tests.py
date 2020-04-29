import pytest
from django.urls import reverse


# class TestAreaViewSet:
#     @pytest.mark.urls('apps.core.api.urls')
#     def test_get_list(self, client):
#         expected_result = 1

#         path = reverse("areas-list")

#         response = client.get(path)

#         assert response.status == 200
#         assert response.json()[0]["id"] == expected_result
