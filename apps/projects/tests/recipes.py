from model_bakery.recipe import Recipe, foreign_key

from apps.utils.baker import get_or_create_foreign_key

from ..lib import constants as projects_constants

generic_company = Recipe(
    "core.Company",
    name="generic-company",
    phone="999999999",
    email="generic@company.com",
    country="VE",
)

generic_user = Recipe(
    "users.User",
    email="john@doe.com",
    name="Jhon Doe",
    company=get_or_create_foreign_key(generic_company),
)

generic_company_project = Recipe(
    "projects.Project",
    name="generic-project",
    company=get_or_create_foreign_key(generic_company),
    kind=projects_constants.ProjectKind.COMPANY.value,
)


generic_normal_project = Recipe(
    "projects.Project",
    name="generic-normal-project",
    company=get_or_create_foreign_key(generic_company),
    kind=projects_constants.ProjectKind.PROJECT.value,
)
