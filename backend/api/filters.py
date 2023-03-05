from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(filters.FilterSet):
    """
    Filter for recipe,
    by tags, favorite list and shoplist.
    """
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug',
                                             to_field_name='slug',
                                             queryset=Tag.objects.all())
    is_favorited = filters.BooleanFilter(method='get_favorite',)
    is_in_shopping_cart = filters.BooleanFilter(method='get_shoplist',)

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'author', 'tags', 'is_in_shopping_cart')

    def get_favorite(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(
                favorite_recipe__user=self.request.user
            )
        return Recipe.objects.all()

    def get_shoplist(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(list__user=self.request.user)
        return Recipe.objects.all()


class IngredFilter(filters.FilterSet):
    """
    Filer for ingredients,
    by name field
    """
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
