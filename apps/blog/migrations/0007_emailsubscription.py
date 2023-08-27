# Generated by Django 4.2.2 on 2023-08-10 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_article_status_alter_article_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=256, unique=True, verbose_name='Email')),
                ('subscription_date', models.DateTimeField(auto_now_add=True, verbose_name='Время подписки')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылка',
            },
        ),
    ]
