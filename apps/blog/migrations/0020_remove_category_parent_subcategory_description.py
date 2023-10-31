# Generated by Django 4.2.2 on 2023-10-29 11:23

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0019_remove_article_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="parent",
        ),
        migrations.AddField(
            model_name="subcategory",
            name="description",
            field=ckeditor_uploader.fields.RichTextUploadingField(default="hello"),
            preserve_default=False,
        ),
    ]