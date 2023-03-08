from django.db import migrations
import json
from pathlib import Path
import os

path = Path(__file__).resolve().parent.parent.parent
file = os.path.join(path, 'data', 'ingredients.json')
with open(file) as json_file:
    INITIAL_INGREDIENTS = json.load(json_file)


def add_ingredient(apps, schema_editor):
    Ingredient = apps.get_model('recipes', 'Ingredient')
    for ingr in INITIAL_INGREDIENTS:
        new_tag = Ingredient(**ingr)
        new_tag.save()


def remove_ingredient(apps, schema_editor):
    Ingredient = apps.get_model('recipes', 'Ingredient')
    for ingr in INITIAL_INGREDIENTS:
        Ingredient.objects.get(name=ingr['name']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_add_tags'),
    ]

    operations = [
        migrations.RunPython(
            add_ingredient,
            remove_ingredient
        )
    ]
