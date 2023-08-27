# Generated by Django 4.2.2 on 2023-08-05 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_article_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('published', 'Опубликовано')], default='draft', max_length=24, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='article',
            name='summary',
            field=models.TextField(default='Краткое содержание', max_length=256, verbose_name='Краткое содержание'),
        ),
    ]
