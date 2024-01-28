from django.db import models


class Notification(models.Model):
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время',
    )
    notifications_message = models.CharField(
        max_length=512,
        verbose_name='Уведомление'
    )
    read = models.BooleanField(default='False', verbose_name='Прочитано')

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f'{self.notifications_message[:128]}'
