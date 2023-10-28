# Generated by Django 4.2.2 on 2023-09-18 17:43

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0015_article_search_vector_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(
                blank=True, null=True
            ),
        ),
    ]