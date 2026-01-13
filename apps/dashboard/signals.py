import logging
from typing import Any
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.website.models import Comment
from .models import Notification
from .templatetags.dashboard_tags import clear_notifications_cache

logger = logging.getLogger('website')


@receiver(post_save, sender=Comment)
def create_comment_notification(
    sender: Comment,
    instance: Notification,
    created: bool,
    **kwargs: Any
    ) -> None:
    """Если был оставлен новый комментарий, то создаётся уведомление."""
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


@receiver([post_save, post_delete], sender=Notification)
def notification_cache_handler(sender, instance, **kwargs) -> None:
    """Очищает кэш уведомлений при их создании, изменении или удалении."""
    try:
        clear_notifications_cache()
        logger.debug(
            f"Кэш уведомлений автоматически очищен после изменения"
        )
    except Exception as e:
        logger.error(
            f"Ошибка автоматической очистки кэша уведомлений: {e}",
            exc_info=True
        )
