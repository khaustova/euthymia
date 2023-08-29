from smtplib import SMTPException
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.urls import reverse
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


@shared_task(name='remove_email')
def remove_email(email):
    """
    Удаляет email из рассылки.
    """
    EmailSubscription.objects.create(email=email)
    return f'Added a new email {email}'


@shared_task(name='send_notification')
def send_notification(article_pk):
    """
    Отправляет уведомление о новой записи на email из рассылки.
    """
    article = Article.objects.get(pk=article_pk)
    connection = get_connection()
    connection.open()
    for email in EmailSubscription.objects.all():
        try:
            subject = '[Euthymia] Опубликована новая запись ' + '«' + article.title + '»'
            message = get_template("manager/emails/notification.html").render(
                {'article': article,
                'email': email.email,
                'email_hash': email.email_hash
                }
            )
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
                reply_to=[settings.EMAIL_HOST_USER]
            )
            mail.content_subtype = 'html'
            mail.send()
        except SMTPException as e:
            continue
    connection.close()
    
    return f'Notifications about new article {article.title} were sent.'


@shared_task(name='add_feedback')
def add_feedback(name, email, message):
    """
    Добавляет новый фидбек.
    """
    Feedback.objects.create(name=name, email=email, message=message)
    return f'Added a new feedback from {name} {email} {message[:50]}'


@shared_task(name='reply_feedback')
def reply_feedback(name, email, reply):
    """
    Отправляет ответ на фидбек.
    """
    subject = 'Subject' 
    message = get_template("manager/emails/reply_feedback.html").render(
        {'name': name, 'reply': reply}
    )
    connection = get_connection()
    connection.open()
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
        reply_to=[settings.EMAIL_HOST_USER]
    )
    mail.content_subtype = 'html'
    mail.send()
    connection.close()
    return f'Feedback was sent.'
