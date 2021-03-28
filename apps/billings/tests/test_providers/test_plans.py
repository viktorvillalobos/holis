import pytest
from djpaddle.models import Plan

from ...providers import plans as plan_providers
from ...tests import baker_recipes as billing_recipes


@pytest.mark.django_db
def test_get_all_paddle_plans():
    plan_price_started = billing_recipes.dj_plan_price_started.make()
    plan_price_pro = billing_recipes.dj_plan_price_pro.make()
    expected_result = [plan_price_started.plan, plan_price_pro.plan]

    assert Plan.objects.count() == 2
    assert plan_price_started.plan.prices.first().quantity == 9.0
    assert plan_price_pro.plan.prices.first().quantity == 49.0

    result = list(plan_providers.get_all_paddle_plans())

    assert len(result) == 2
    assert expected_result == list(result)
