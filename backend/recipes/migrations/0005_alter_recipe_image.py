# Generated by Django 3.2.18 on 2023-03-03 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20230302_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='back_media/recipes/media/', verbose_name='Image'),
        ),
    ]
