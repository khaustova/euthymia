# Generated by Django 4.2.2 on 2025-01-22 20:41

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0021_sitesettings_about_me_sitesettings_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="about_site",
            field=ckeditor_uploader.fields.RichTextUploadingField(
                blank=True, null=True, verbose_name="О сайте (шапка)"
            ),
        ),
    ]
