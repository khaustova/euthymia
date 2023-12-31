# Generated by Django 4.2.2 on 2023-06-23 18:33

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('summary', models.TextField(default='Краткое содержание', max_length=230, verbose_name='Краткое содержание')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField()),
                ('image', models.ImageField(blank=True, upload_to='uploads/', verbose_name='Изображение')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Время редактирования')),
                ('slug', models.SlugField(unique=True, verbose_name='url')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')),
                ('keywords', models.CharField(blank=True, help_text='Перечислите ключевые слова через запятую.', max_length=256, verbose_name='Ключевые слова')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Тег')),
                ('slug', models.SlugField(unique=True, verbose_name='url')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', imagekit.models.fields.ProcessedImageField(blank=True, default='avatars/avatar.jpg', upload_to='avatars/', verbose_name='Аватар')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest', models.CharField(blank=True, max_length=250, null=True, verbose_name='Гость')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('body', models.TextField(max_length=800, verbose_name='Комментарий')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.article', verbose_name='Статья')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blog.comment', verbose_name='Родительский комментарий')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['created_date'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Категория')),
                ('slug', models.SlugField(unique=True, verbose_name='url')),
                ('description', models.TextField(max_length=256, verbose_name='Описание')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blog.category', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='blog.tag', verbose_name='Теги'),
        ),
    ]
