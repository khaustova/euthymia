# Generated by Django 4.2.2 on 2023-08-26 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='notifications_item',
        ),
        migrations.AddField(
            model_name='notification',
            name='notifications_model',
            field=models.CharField(default='a', max_length=512, verbose_name='Модель'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='notifications_model_pk',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
    ]
