# Generated by Django 4.2.2 on 2024-02-12 15:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0027_article_is_draft"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="slug",
            field=models.SlugField(default=1, unique=True, verbose_name="url"),
            preserve_default=False,
        ),
    ]
