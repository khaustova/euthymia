from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article
    
@receiver(post_save, sender=Article)
def post_save_artcile(sender, instance, created, update_fields, **kwargs):
    instance.update_search_vector()