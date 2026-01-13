
from typing import Any
from django.db.models.signals import post_save, pre_save
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
    """Обновляет поисковый вектор при создании новой статьи."""
    instance.update_search_vector()

    
@receiver(pre_save, sender=Article)
def pre_save_artcile(
    sender: Article, 
    instance: Article, 
    update_fields: list, 
    **kwargs : Any
):
    """Обновляет номер статьи для сортировки."""
    article_number = instance.title.split()[0]

    try:
        main_number = int(article_number.split('.')[0])
    except:
        main_number = 0
        
    try:
        sub_number = int(article_number.split('.')[1])
    except:
        sub_number = 0
    
    instance.main_number = main_number
    instance.sub_number = sub_number