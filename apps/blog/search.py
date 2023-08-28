# from elasticsearch_dsl.query import Q, MultiMatch
# from .documents import ArticleDocument


# def get_search_query(phrase):
#     query = Q(
#         'function_score', 
#         query=MultiMatch(
#             fields=['title', 'body'], query=phrase
#         ),
#     )
#     return ArticleDocument.search().query(query)


# def search(phrase):
#     return get_search_query(phrase).to_queryset()

def search(phrase):
    return
