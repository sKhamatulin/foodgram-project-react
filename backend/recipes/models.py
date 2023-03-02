from django.db import models

from django.contrib.auth import get_user_model

LINE_SLICE = 50
User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Name',
        unique=True,
        max_length=16,)
    color = models.CharField(
        max_length=16,
        verbose_name='Color',)
    slug = models.SlugField(
        max_length=16,
        unique=True,
        verbose_name='Slug',)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Name of ingredient',
        max_length=100,)
    measurement_unit = models.CharField(
        verbose_name='Unit of metr',
        max_length=15,)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredientes'

    def __str__(self):
        return f'{self.name} --- {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',)
    name = models.CharField(
        verbose_name='Name',
        max_length=200,)
    image = models.ImageField(
        verbose_name='Image',
        upload_to='recipes/media/',)
    text = models.TextField(
        verbose_name='Discription',)
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ingredientes',
        through='IngredInRecipe',
        related_name='recipe',)
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags',
        related_name='recipes',)
    cooking_time = models.IntegerField(
        verbose_name='Cooking time',)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date of publish',)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f'{self.name[:LINE_SLICE]}'


class IngredInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Recipe',
        related_name='recipe_ingredient',)
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ingredient is recipe',)
    amount = models.PositiveSmallIntegerField(
        verbose_name='Amount',)

    class Meta:
        verbose_name = 'Amount of Ingredient'
        verbose_name_plural = 'Amount of Ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique ingredient for recipe'
            )
        ]

    def __str__(self):
        return (f'{self.recipe}: {self.ingredient.name},'
                f' {self.amount}, {self.ingredient.measurement_unit}')


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Recipes',
        related_name='favorite',
        on_delete=models.CASCADE,)
    user = models.ForeignKey(
        User,
        verbose_name='User',
        related_name='how_favorite',
        on_delete=models.CASCADE,)

    class Meta:
        verbose_name = 'Favorite Recipe'
        verbose_name_plural = 'Favorite Recipes'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique favorite'),
        )

    def __str__(self):
        return f'{self.recipe} is in {self.user}\'s favorite list'


class ShoppingList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Recipes',
        related_name='shopping_list',
        on_delete=models.CASCADE,)
    user = models.ForeignKey(
        User,
        verbose_name='User',
        related_name='how_shopping_list',
        on_delete=models.CASCADE,)

    class Meta:
        verbose_name = 'Recipe in cart'
        verbose_name_plural = 'Recipe in carts'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique recipe in shoplist'),
        )

    def __str__(self):
        return f'{self.recipe} is in the {self.user} cart'
