from .. import services as billing_services


def test_get_paddle_plans_sorted_by_price(mocker):
    mocked_provider = mocker.patch(
        "apps.billings.services.plan_providers.get_all_paddle_plans"
    )

    result = billing_services.get_paddle_plans_sorted_by_price()
    mocked_provider.assert_called_once()

    assert isinstance(result, list)


def test_get_total_current_full_plan_subcriptions(mocker):
    mocked_provider = mocker.patch(
        "apps.billings.services.plan_subscriptions.get_total_current_full_plan_subscriptions"
    )
    result = billing_services.get_total_current_full_plan_subscriptions()
    mocked_provider.assert_called_once()
