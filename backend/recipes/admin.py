from django.contrib import admin

from .models import (Recipe, Ingredient, Tag,
                     IngredInRecipe, Favorite, ShoppingList)


class IngredientInline(admin.TabularInline):
    model = IngredInRecipe


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'text',
                    'cooking_time', 'favorited')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-empty-'

    inlines = [
        IngredientInline,
    ]

    def favorited(self, obj):
        favorited_count = Favorite.objects.filter(recipe=obj).count()
        return favorited_count

    favorited.short_description = 'Is in favorite'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")
    empty_value_display = '-empty-'


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    empty_value_display = '-empty-'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)