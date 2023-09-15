from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import GinIndex
from django.urls import reverse_lazy
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel, TreeForeignKey
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class UserProfile(models.Model):
    """
    Модель, расширяющая стандартную модель пользователя возможностью добавления
    аватара.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = ProcessedImageField(
        upload_to='avatars/',
        verbose_name='Аватар',
        default='static/blog/img/admin_avatar.png',
        processors=[ResizeToFill(50, 50)],
        blank=True
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username


class Category(MPTTModel):
    name = models.CharField(max_length=128, verbose_name='Категория')
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Родительская категория',
        related_name='children'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('blog:category', kwargs={'slug': self.slug})

    def get_article_list(self):
        return Article.objects.filter(category=self)


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    summary = models.TextField(
        max_length=256,
        default='Краткое содержание',
        verbose_name='Краткое содержание'
    )
    body = RichTextUploadingField()
    image = models.ImageField(
        upload_to='uploads/',
        blank=True,
        verbose_name='Изображение',
    )
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
        verbose_name='Категория',
    )
    views = models.PositiveIntegerField(
        verbose_name='Количество просмотров',
        default=0
    )
    keywords = models.CharField(
        verbose_name='Ключевые слова',
        max_length=256,
        blank=True,
        help_text='Перечислите ключевые слова через запятую.'
    )
    next_article = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='next_articles',
        verbose_name='Следующая статья'
    )
    prev_article = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='prev_articles',
        verbose_name='Предыдущая статья'
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
        return reverse_lazy('blog:article_detail', kwargs={'slug': self.slug})
    
    def update_search_vector(self):
            qs = Article.objects.filter(pk=self.pk)
            qs.update(search_vector=SearchVector('title', 'body'))


class Comment(MPTTModel):
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
        return f'Комментарий {self.body[:60]}'
