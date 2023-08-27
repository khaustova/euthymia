from smtplib import SMTPException
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.template.loader import get_template
from celery import shared_task
from blog.models import Article
from manager.models import EmailSubscription, Feedback


@shared_task(name='add_email')
def add_email(email):
    """
    Добавляет email в рассылку.
    """
    EmailSubscription.objects.create(email=email)
    return f'Added a new email {email}'


@shared_task(name='add_feedback')
def add_feedback(name, email, message):
    """
    Добавляет новый фидбек.
    """
    Feedback.objects.create(name=name, email=email, message=message)
    return f'Added a new feedback {message[:50]}'


@shared_task(name='send_notification')
def send_notification(article_pk):
    """
    Отправляет уведомление о новой записи на email из рассылки.
    """
    article = Article.objects.get(pk=article_pk)
    subject = 'Subject' 
    message = get_template("manager/emails/notification.html").render({'article': article})
    connection = get_connection()
    connection.open()
    for email in EmailSubscription.objects.all():
        mail = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
            reply_to=[settings.EMAIL_HOST_USER]
        )
        mail.content_subtype = 'html'
        try:
            mail.send()
        except SMTPException as e:
            continue
    connection.close()
    return f'Notifications about new article {article.title} were sent.'