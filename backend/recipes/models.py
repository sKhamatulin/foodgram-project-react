from django.db import models

from users.models import User

LINE_SLICE = 50


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Name',
        unique=True,
        max_length=16,

    )
    color = models.CharField(
        max_length=16,
        verbose_name='Color'
    )
    slug = models.SlugField(
        max_length=16,
        unique=True,
        verbose_name='Slug',
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Name of ingredient',
        max_length=100
    )
    measurement_unit = models.CharField(
        verbose_name='Unit of metr',
        max_length=15
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredientes'

    def __str__(self):
        return f'{self.measurement_unit}, {self.name}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        verbose_name='Name',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Image',
        upload_to='recipes/'
    )
    text = models.TextField(
        verbose_name='Discription'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ingredientes',
        through='RecipeIngredient',
        related_name='recipe'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags',
        related_name='recipes'
    )
    cooking_time = models.IntegerField(
        verbose_name='Cooking time',
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Date of publish'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f'{self.name[:LINE_SLICE]}'
