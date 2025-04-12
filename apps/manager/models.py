from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class EmailSubscription(models.Model):
    email = models.EmailField(
        max_length=256,
        null=False,
        unique=True,
        verbose_name='Email'
    )
    email_hash = models.CharField(max_length=256, blank=True, null=True)
    subscription_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата подписки',
    )

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылка'

    def __str__(self):
        return self.email


class Feedback(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя')
    email = models.EmailField(max_length=256, verbose_name='Email')
    feedback_ip = models.CharField(max_length=256, verbose_name='IP-адрес')
    message = models.TextField(verbose_name='Сообщение')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    reply = RichTextUploadingField()
    reply_status = models.BooleanField(
        default=False,
        verbose_name='Статус ответа'
    )

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return f'{self.name}: {self.message[:50]}'


class SiteSettings(models.Model):
    about_me = RichTextUploadingField(
        blank=True, 
        null=True, 
        verbose_name='Описание сайта'
    )
    is_subscribe = models.BooleanField(
        verbose_name = 'Возможность подписки'
    )

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return 'Настройки сайта'
