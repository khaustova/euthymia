from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Article


# @registry.register_document
# class ArticleDocument(Document):
#     body = fields.TextField(attr=None)
    
#     class Index:
#         name = 'articles'
#         settings = {'number_of_shards': 1,
#                     'number_of_replicas': 0}

#     class Django:
#         model = Article
#         fields = [
#             'title',
#             'created_date',
#             'slug',
#         ]