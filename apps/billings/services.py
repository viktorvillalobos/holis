from apps.utils.cache import DAY, cache
from apps.utils.dataclasses import build_dataclass_from_model_instance

from .lib.dataclasses import PaddlePlanData
from .providers import plans as plan_providers
from .providers import subscriptions as plan_subscriptions


@cache(DAY)
def get_paddle_plans_sorted_by_price() -> list[PaddlePlanData]:
    """
    Returns a list of paddle plans ordered by price

    Observation: before using this plans must be sync using
    the paddle manage.py command
    """
    plans = plan_providers.get_all_paddle_plans()

    plans_list = []
    for plan in plans:
        price = plan.prices.latest("id").quantity
        plans_list.append(
            build_dataclass_from_model_instance(
                klass=PaddlePlanData, instance=plan, price=int(price)
            )
        )

    return sorted(plans_list, key=lambda item: item.price)


def get_total_current_full_plan_subscriptions() -> int:
    return plan_subscriptions.get_total_current_full_plan_subscriptions()
