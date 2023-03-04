# Generated by Django 3.2.18 on 2023-03-02 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_add_ingredients'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ingredinrecipe',
            name='unique ingredient for recipe',
        ),
        migrations.AlterField(
            model_name='ingredinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Recipe'),
        ),
        migrations.AddConstraint(
            model_name='ingredinrecipe',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique ingredient for recipe'),
        ),
    ]