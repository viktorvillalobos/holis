from model_bakery import baker
from model_bakery.recipe import Recipe


class GetOrCreateRecipe(Recipe):
    def __init__(self, recipe: Recipe, **kwargs):
        if not isinstance(recipe, Recipe):
            raise TypeError("Not a recipe")

        finder = baker.ModelFinder()
        model = finder.get_model(recipe._model)

        self._queryset = model.objects.filter(**kwargs)
        self._recipe = recipe

    def make(self):
        return self._queryset.first() or self._recipe.make()


class GetOrCreateForeignKey(object):
    def __init__(self, recipe: Recipe, **kwargs):
        self.recipe = GetOrCreateRecipe(recipe, **kwargs)

    def __call__(self):
        return self.recipe.make()


def get_or_create_foreign_key(recipe: Recipe, **kwargs) -> GetOrCreateForeignKey:
    return GetOrCreateForeignKey(recipe, **kwargs)


def get_or_create_related_item(recipe: Recipe, **kwargs) -> GetOrCreateRecipe:
    return GetOrCreateRecipe(recipe, **kwargs)
