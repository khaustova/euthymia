# from elasticsearch_dsl.query import Q, MultiMatch
# from .documents import ArticleDocument


# def get_search_query(phrase: str) -> ArticleDocument:
#     query = Q(
#         'function_score',
#         query=MultiMatch(
#             fields=['title', 'body'], query=phrase
#         ),
#     )
#     return ArticleDocument.search().query(query)


def search(phrase: str):
    return
    # return get_search_query(phrase).to_queryset()
