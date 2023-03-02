from django.db import migrations

INITIAL_TAGS = [
    {'color': 'orange', 'name': 'breakfast', 'slug': 'breakfast'},
    {'color': 'green', 'name': 'lunch', 'slug': 'lunch'},
    {'color': 'purple', 'name': 'dinner', 'slug': 'dinner'},
]


def add_tags(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    for tag in INITIAL_TAGS:
        new_tag = Tag(**tag)
        new_tag.save()


def remove_tags(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    for tag in INITIAL_TAGS:
        Tag.objects.get(name=tag['name']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_tags,
            remove_tags
        )
    ]
