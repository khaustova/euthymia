# Generated by Django 4.2.2 on 2023-08-26 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_tag_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='status',
        ),
    ]
