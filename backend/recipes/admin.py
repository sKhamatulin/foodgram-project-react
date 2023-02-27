from django.contrib import admin

from .models import (Recipe, Ingredient, Tag,
                     IngredInRecipe, Favorite, ShoppingList)


admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(IngredInRecipe)
admin.site.register(Favorite)
admin.site.register(ShoppingList)