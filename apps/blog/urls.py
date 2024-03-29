from django.urls import path
from django.views.generic import TemplateView
from apps.blog.views import (
    ArticleView,
    ArticleDetailView,
    SearchView,
    subscribe_form,
    unsubscribe,
    feedback_form,
    get_subcategory
)

app_name = 'blog'

urlpatterns = [
    path('', ArticleView.as_view(), name='index'),
    path('hot/', ArticleView.as_view(), {'sort': 'views'}, name='hot_index'),
    path('<slug:category>/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('subscribe/', subscribe_form, name='subscribe'),
    path('unsubscribe/', unsubscribe, name='unsubscribe'),
    path('feedback/', feedback_form, name='feedback'),
    path('about/', TemplateView.as_view(template_name="blog/about.html"), name='about'),
    path('getsubcategory/', get_subcategory, name='get-subcategory'),
]
