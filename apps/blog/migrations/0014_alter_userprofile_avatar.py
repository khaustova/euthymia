# Generated by Django 4.2.2 on 2023-09-01 10:31

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_remove_article_tags_remove_category_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='static/blog/img/admin_avatar.png', upload_to='avatars/', verbose_name='Аватар'),
        ),
    ]
