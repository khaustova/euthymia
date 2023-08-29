from django.db import models
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
    reply = models.TextField(blank='True', null='True', verbose_name='Ответ')
    reply_status = models.BooleanField(default=False, verbose_name='Статус ответа')
    
    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
     
    def __str__(self):
        return f'{self.name}: {self.message[:50]}'
    
    
class AboutSite(models.Model):
    about_site = RichTextUploadingField()
    
    class Meta:
        verbose_name = 'О сайте'
        verbose_name_plural = 'О сайте'
     
    def __str__(self):
        return f'Описание сайта'