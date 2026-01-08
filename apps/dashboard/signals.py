from typing import Any
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.blog.models import Comment
from apps.dashboard.models import Notification

@receiver(post_save, sender=Comment)
def create_comment_notification(
    sender: Comment,
    instance: Notification,
    created: bool,
    **kwargs: Any
    ) -> None:
    """
    Если гостем был оставлен новый комментарий, то создаётся соответствующее
    уведомление.
    """
    if created:
        if instance.guest:
            url = instance.article.get_absolute_url()
            Notification.objects.create(
                notifications_message='Новый комментарий от '
                + instance.guest
                + ' к <strong><a href="'
                + url
                + '" class="notification__link"> статье '
                + instance.article.title
                + '</a></strong>'
            )
