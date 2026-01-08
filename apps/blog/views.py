from akismet import Akismet
from json import dumps
from typing import Any, Callable
from ipware import get_client_ip

from django.conf import settings
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.http import (
    HttpRequest, 
    HttpResponse, 
    HttpResponseForbidden, 
    HttpResponseRedirect, 
    Http404
)
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View

from .models import Article, Comment, Category, Subcategory, Status
from .forms import CommentForm


class ArticleView(ListView):
    """
    Отображает список опубликованных статей по популярности или по дате.
    """
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = 10
    paginate_orphans = 5

    def get_queryset(self):
        """
        Возвращает список опубликованных статей по популярности или по дате.
        """
        sort = self.kwargs.get('sort')
        if sort == 'views':
            return Article.objects.filter(
                status=Status.PUBLISHED
            ).order_by('-views', 'created_date')
        return Article.objects.filter(status=Status.PUBLISHED).order_by('-created_date')


class ArticleDetailView(DetailView):
    """
    Отображает информацию о статье.
    """
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs: Any) -> dict:
        """
        Добавляет в контекст данные о комментариях к статье, их количестве 
        и форме для отправки комментариев.
        """
        context = super().get_context_data()
        context['comments'] = Comment.objects.filter(article=self.get_object())
        context['comments_number'] = context['comments'].count()
        context['form'] = CommentForm()
        return context

    def post(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any
    ) -> HttpResponseRedirect:
        """
        Обрабатывает отправку комментариев.
        Если включена проверка на спам с помощью Akismet, то проверяет данные перед
        их сохранением.
        """
        if self.request.method == 'POST':
            comment_form = CommentForm(self.request.POST)
            if comment_form.is_valid():     
                new_comment = comment_form.save(commit=False)
                if self.request.user.is_authenticated:
                    new_comment.author = self.request.user
                    new_comment.email = self.request.user.email
                else:
                    guest = comment_form.cleaned_data.get('guest')
                    if guest:
                        new_comment.guest = comment_form.cleaned_data.get('guest')
                    else:
                        new_comment.guest = 'Безымянный'
                    new_comment.email = comment_form.cleaned_data.get('email')

                client_ip, is_routable = get_client_ip(request)
                if client_ip is None:
                    new_comment.comment_ip = 'Unable'
                else:
                    if is_routable:
                        new_comment.comment_ip = client_ip
                    else:
                        new_comment.comment_ip = 'Private'

                if settings.IS_USE_AKISMET:
                    akismet_api = Akismet(
                        key=settings.AKISMET_API_KEY, 
                        blog_url=settings.AKISMET_BLOG_URL
                    )
                    is_spam = akismet_api.comment_check(
                        user_ip=new_comment.comment_ip,
                        user_agent=request.META.get('HTTP_USER_AGENT'),
                        comment_type='comment',
                        comment_author=new_comment.author,
                        comment_author_email=new_comment.email,
                        comment_content=comment_form.cleaned_data.get('body'),
                    )

                    if is_spam:
                        return HttpResponseForbidden('Упс! Доступ запрещён!')                 

                new_comment.article = self.get_object()
                new_comment.save()
            return redirect(self.request.path_info + '#comments')

    def dispatch(
        self,
        request: HttpRequest,
        slug: str,
        *args: Any,
        **kwargs: Any
    ) -> Callable:
        """
        Увеличивает количество просмотров статьи при её открытии.
        """
        obj = self.get_object()
        obj.views += 1
        obj.save()
        return super().dispatch(request, *args, **kwargs)


class CategoryRedirectView(View):
    """
    Находит первую статью в указанной категории и перенаправляет на нее.
    """
    def get(self, request, category):
        try:
            first_article = Article.objects.filter(category__slug=category).order_by('created_date').first()
            
            if first_article:
                return redirect('blog:article_detail', category, first_article.slug)
            else:
                raise Http404('В этой категории нет статей.')
                
        except Article.DoesNotExist:
            raise Http404('Категория не найдена или в ней нет статей.')


class SearchView(ListView):
    """
    Отображает список опубликованных в соответствии с запросом.
    """
    model = Article
    context_object_name = 'articles'
    template_name = 'blog/search_results.html'
    paginate_by = 10
    paginate_orphans = 5

    def get_queryset(self) -> Article:
        """
        Возвращает список статей в соответствии с запросом.
        """
        query = self.request.GET.get('query')
        search_vector = SearchVector('title', 'body')
        search_query = SearchQuery(query)
        return (
            Article.objects.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            )
            .filter(search=search_query, status=Status.PUBLISHED)
            .order_by("-rank")
        )


def get_subcategory(request):
    """
    В формате JSON возвращает только те подкатегории, что принадлежат 
    выбранной категориии. Используется при создании статьи.
    """
    id = request.GET.get('id', '')
    target_category = Category.objects.get(pk=id)
    result = list(Subcategory.objects.filter(
        category=target_category).values('id', 'name')
    )

    return HttpResponse(dumps(result), content_type='application/json')
