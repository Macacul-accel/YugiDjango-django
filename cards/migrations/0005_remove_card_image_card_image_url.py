# Generated by Django 5.1.6 on 2025-03-12 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_alter_deckcard_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='image',
        ),
        migrations.AddField(
            model_name='card',
            name='image_url',
            field=models.URLField(db_index=True, null=True),
        ),
    ]
