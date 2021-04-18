from model_bakery.recipe import Recipe

from apps.utils.baker import get_or_create_foreign_key

adslab = Recipe("core.Company", name="Adslab", code="adslab", country="VE")


default_area = Recipe(
    "core.Area", name="default", company=get_or_create_foreign_key(adslab)
)
