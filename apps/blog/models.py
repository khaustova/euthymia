from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import GinIndex
from django.urls import reverse, reverse_lazy
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey


class UserProfile(models.Model):
    """
    Модель, расширяющая стандартную модель пользователя возможностью добавления
    аватара.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='avatars/',
        verbose_name='Аватар',
        blank=True
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username


class Category(models.Model):
    """
    Модель категории статьи.
    """
    name = models.CharField(max_length=256, verbose_name='Категория')
    slug = models.SlugField(unique=True, verbose_name='url')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """
    Модель подкатегории статьи.
    """
    name = models.CharField(max_length=256, verbose_name='Подкатегория')
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Status(models.TextChoices):
    """
    Модель статуса статьи.
    """
    DRAFT = 'draft', 'Черновик'
    PUBLISHED = 'published', 'Опубликовано' 


class Article(models.Model):
    """
    Модель статьи.
    """
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    summary = models.TextField(verbose_name='Краткое содержание')
    body = RichTextUploadingField(verbose_name='Текст статьи')
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Время редактирования',
    )
    slug = models.SlugField(unique=True, verbose_name='url')
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Категория',
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Подкатегория',
    )
    status = models.CharField(
        max_length=64,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Статус'
    )
    views = models.PositiveIntegerField(
        verbose_name='Количество просмотров',
        default=0
    )
    description = models.TextField(
        verbose_name='Мета-описание',
        blank=True,
    )
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['title']
        indexes = [
            GinIndex(fields=['search_vector',]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy(
            'blog:article_detail', 
            kwargs={'slug': self.slug, 'category': self.category.slug}
        )

    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=(self.id,))

    def update_search_vector(self):
        qs = Article.objects.filter(pk=self.pk)
        qs.update(search_vector=SearchVector('title', 'body'))


class Comment(MPTTModel):
    """
    Модель комментария к статье.
    """
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='Статья'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Автор'
    )
    guest = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name='Гость'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='Email'
    )
    comment_ip = models.CharField(max_length=256, verbose_name='IP-адрес')
    body = models.TextField(max_length=800, verbose_name='Комментарий')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Родительский комментарий',
        related_name='children'
    )

    class MTTMeta:
        order_insertion_by = ('created_date',)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_date']

    def __str__(self):
        return f'{self.body[:256]}'

    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=(self.id,))
