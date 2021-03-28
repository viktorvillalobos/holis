import responses

from ... import paddle_endpoints
from ...providers import subscriptions as subscriptions_providers


@responses.activate
def test_get_total_current_full_plan_subscriptions(mocker):
    responses.add(
        responses.POST,
        paddle_endpoints.SUBCSCRIPTION_USERS,
        json={"response": [{"a": 1}, {"b": 2}]},
    )

    result = subscriptions_providers.get_total_current_full_plan_subscriptions()

    assert result == 2
