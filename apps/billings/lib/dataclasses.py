from dataclasses import dataclass


@dataclass
class PaddlePlanData:
    name: str
    billing_type: str
    billing_period: int
    trial_days: int
    price: float
