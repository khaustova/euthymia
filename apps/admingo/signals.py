from django.db.models.signals import post_save
from django.dispatch import receiver
from manager.models import Feedback
from blog.models import Comment
from admingo.models import Notification


@receiver(post_save, sender=Feedback)
def create_feedback_notification(sender, instance, created, **kwargs):
    """
    Если с помощью обратной связи было получено сообщение, то создаётся 
    соответствующее уведомление.
    """
    if created:        
        Notification.objects.create(
            notifications_message = '<strong><a href="/admin/manager/feedback/" class="notification__link">Новое сообщение</a></strong> от ' + instance.name)
        
        
@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """
    Если гостем был оставлен новый комментарий, то создаётся соответствующее 
    уведомление.
    """
    if created:    
        if instance.guest:   
            url = instance.article.get_absolute_url()
            print(url)
            Notification.objects.create(
                notifications_message = 'Новый комментарий от ' 
                + instance.guest + ' к '
                + '<strong><a href="' + instance.article.get_absolute_url() + '" class="notification__link"> статье ' + instance.article.title +'</a></strong>')
