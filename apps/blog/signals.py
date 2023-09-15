
from typing import Any
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article
    
@receiver(post_save, sender=Article)
def post_save_artcile(
    sender: Article, 
    instance: Article, 
    created: bool, 
    update_fields: list, 
    **kwargs : Any
):
    instance.update_search_vector()