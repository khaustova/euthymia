from django.urls import path
from blog.views import (
    ArticleView, 
    ArticleDetailView, 
    CategoryView, 
    TagView, 
    SearchView, 
    subscribe_form, 
    feedback_form
)

app_name = 'blog'

urlpatterns = [
    path('', ArticleView.as_view(), name='index'),
    path('hot/', ArticleView.as_view(), {'sort': 'views'}, name='hot_index'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('category/<slug:slug>/hot/', CategoryView.as_view(), {'sort': 'views'}, name='hot_category'),
    path('tag/<slug:slug>/', TagView.as_view(), name='tag'),
    path('tag/<slug:slug>/hot/', TagView.as_view(), {'sort': 'views'}, name='hot_tag'),
    path('search/', SearchView.as_view(), name='search'),
    path('subscribe/', subscribe_form, name='subscribe'),
    path('feedback/', feedback_form, name='feedback'),
]
