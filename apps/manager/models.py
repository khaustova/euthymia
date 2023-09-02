from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField 

class EmailSubscription(models.Model):
    email = models.EmailField(
        max_length=256, 
        null=False, 
        unique=True, 
        verbose_name='Email'
    ) 
    email_hash = models.CharField(blank=True, null=True)
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
    message = models.TextField(verbose_name='Сообщение')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    reply = RichTextUploadingField()
    reply_status = models.BooleanField(default=False, verbose_name='Статус ответа')
    
    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
     
    def __str__(self):
        return f'{self.name}: {self.message[:50]}'
    
    
class SiteDescription(models.Model):
    site_description = RichTextUploadingField()
    site_image = ProcessedImageField(
        upload_to='uploads/', 
        verbose_name='Аватар',
        default='/static/blog/img/admin_avatar.png',
        processors=[ResizeToFill(50, 50)],
        blank=True
    )
    
    class Meta:
        verbose_name = 'О сайте'
        verbose_name_plural = 'О сайте'
     
    def __str__(self):
        return f'Описание сайта'
