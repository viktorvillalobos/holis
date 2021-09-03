from model_bakery.recipe import Recipe

from apps.core.tests import baker_recipes as core_recipes
from apps.core.tests.baker_recipes import adslab
from apps.utils.baker import get_or_create_foreign_key

user_viktor = Recipe(
    "users.User",
    name="Víktor",
    company=get_or_create_foreign_key(adslab),
    current_area=get_or_create_foreign_key(core_recipes.default_area),
)


user_julls = Recipe(
    "users.User",
    name="Julls",
    company=get_or_create_foreign_key(adslab),
    current_area=get_or_create_foreign_key(core_recipes.default_area),
)

user_tundi = Recipe(
    "users.User",
    name="Tundi",
    company=get_or_create_foreign_key(adslab),
    current_area=get_or_create_foreign_key(core_recipes.default_area),
)

user_joel = Recipe(
    "users.User",
    name="Joel",
    company=get_or_create_foreign_key(adslab),
    current_area=get_or_create_foreign_key(core_recipes.default_area),
)

user_status_holidays = Recipe(
    "users.Status",
    company=get_or_create_foreign_key(adslab),
    user=get_or_create_foreign_key(user_viktor),
    text="holidays",
    is_active=True,
)
