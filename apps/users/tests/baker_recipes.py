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
    name="Víktor",
    company=get_or_create_foreign_key(adslab),
    current_area=get_or_create_foreign_key(core_recipes.default_area),
)
