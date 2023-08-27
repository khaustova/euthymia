from django.apps import AppConfig
from django.conf import settings
from elasticsearch_dsl.connections import connections


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Блог'
    
    def ready(self):
        connections.configure(**settings.ELASTICSEARCH_DSL)
