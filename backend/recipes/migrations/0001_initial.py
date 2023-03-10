# Generated by Django 2.2.19 on 2023-03-01 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name of ingredient')),
                ('measurement_unit', models.CharField(max_length=15, verbose_name='Unit of metr')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredientes',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='IngredInRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(verbose_name='Amount')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Ingredient', verbose_name='Ingredient is recipe')),
            ],
            options={
                'verbose_name': 'Amount of Ingredient',
                'verbose_name_plural': 'Amount of Ingredients',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('image', models.ImageField(upload_to='recipes/media/', verbose_name='Image')),
                ('text', models.TextField(verbose_name='Discription')),
                ('cooking_time', models.IntegerField(verbose_name='Cooking time')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Date of publish')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='??????????')),
                ('ingredients', models.ManyToManyField(related_name='recipe', through='recipes.IngredInRecipe', to='recipes.Ingredient', verbose_name='Ingredientes')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='Name')),
                ('color', models.CharField(max_length=16, verbose_name='Color')),
                ('slug', models.SlugField(max_length=16, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list', to='recipes.Recipe', verbose_name='Recipes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='how_shopping_list', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Recipe in cart',
                'verbose_name_plural': 'Recipe in carts',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='ingredinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredient', to='recipes.Recipe', verbose_name='Recipe'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='recipes.Recipe', verbose_name='Recipes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='how_favorite', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Favorite Recipe',
                'verbose_name_plural': 'Favorite Recipes',
            },
        ),
        migrations.AddConstraint(
            model_name='shoppinglist',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique recipe in shoplist'),
        ),
        migrations.AddConstraint(
            model_name='ingredinrecipe',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique ingredient for recipe'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique favorite'),
        ),
    ]
