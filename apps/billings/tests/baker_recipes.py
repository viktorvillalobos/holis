from model_bakery.recipe import Recipe, foreign_key, related

dj_plan_started = Recipe(
    "djpaddle.Plan",
    name="Started",
    billing_type="month",
    billing_period=30,
    trial_days=7,
)

dj_plan_pro = Recipe(
    "djpaddle.Plan", name="Pro", billing_type="month", billing_period=30, trial_days=7
)

dj_plan_price_started = Recipe(
    "djpaddle.Price",
    currency="USD",
    quantity=9,
    recurring=True,
    plan=foreign_key(dj_plan_started),
)

dj_plan_price_pro = Recipe(
    "djpaddle.Price",
    currency="USD",
    quantity=49,
    recurring=True,
    plan=foreign_key(dj_plan_pro),
)
