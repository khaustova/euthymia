from django.urls import path
from .views import reply_feedback

app_name = 'manager'

urlpatterns = [
    path('feedback/<int:id>/reply/', reply_feedback, name='reply_feedback'),
]