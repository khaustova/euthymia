from django.urls import path
from apps.website.views import (
    ArticleView,
    ArticleDetailView,
    CategoryRedirectView,
    SearchView,
    get_subcategory
)

app_name = 'website'

urlpatterns = [
    path('', ArticleView.as_view(), name='index'),
    path('hot/', ArticleView.as_view(), {'sort': 'views'}, name='hot_index'),
    path('<slug:category>/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<slug:category>/', CategoryRedirectView.as_view(), name='category_redirect'),
    path('search/', SearchView.as_view(), name='search'),
    path('getsubcategory/', get_subcategory, name='get-subcategory'),
]
