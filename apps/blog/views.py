from akismet import Akismet
from json import dumps
from typing import Any, Callable
from ipware import get_client_ip

from django.conf import settings
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from manager.tasks import add_email, add_feedback
from manager.models import EmailSubscription

from .models import Article, Comment, Category, Subcategory
from .forms import CommentForm, SubscribeForm, FeedbackForm


class ArticleView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = 10
    paginate_orphans = 5
    
    def get_queryset(self):
        sort = self.kwargs.get('sort')
        if sort == 'views':
            return Article.objects.filter(is_draft=False).order_by('-views', 'created_date')
        return Article.objects.filter(is_draft=False).order_by('-created_date')
    

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data()
        context['comments'] = Comment.objects.filter(article=self.get_object())
        context['comments_number'] = context['comments'].count()
        context['form'] = CommentForm()
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseRedirect:
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
                        return HttpResponseForbidden('Упс! Недостаточно прав!')                 
                        
                new_comment.article = self.get_object()
                new_comment.save()
            return redirect(self.request.path_info)

    def dispatch(self, request: HttpRequest, slug: str, *args: Any, **kwargs: Any) -> Callable:
        obj = self.get_object()
        obj.views += 1
        obj.save()
        return super().dispatch(request, *args, **kwargs)


class SearchView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'blog/search.html'
    paginate_by = 10
    paginate_orphans = 5

    def get_queryset(self) -> Article:
        query = self.request.GET.get('query')
        search_vector = SearchVector('title', 'body')
        search_query = SearchQuery(query)
        return (
            Article.objects.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            )
            .filter(search=search_query, is_draft=False)
            .order_by("-rank")
        )


def feedback_form(request: HttpRequest) -> HttpResponse:
    """
    Получает заполненную форму обратной связи и передаёт данные из неё в зада-
    чу, отвечающую за добавление их в базу данных.
    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            client_ip, is_routable = get_client_ip(request)
            if client_ip is None:
                feedback_ip = 'Unable'
            else:
                if is_routable:
                    feedback_ip = client_ip
                else:
                    feedback_ip = 'Private'
            
            add_feedback.delay(name, email, feedback_ip, message)
    return render(request, 'blog/feedback_success.html')


def subscribe_form(request: HttpRequest) -> HttpResponse:
    """
    Получает заполненную форму подписки на блог и передаёт данные из неё в
    задачу, отвечающую за добавление email в базу данных.
    """
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            add_email.delay(email)
    return render(request, 'blog/subscribe_success.html')


def get_subcategory(request):
    """
    В формате JSON возвращает только те подкатегории, что принадлежат 
    выбранной категориии. Используется при создании статьи.
    """
    id = request.GET.get('id', '')
    target_category = Category.objects.get(pk=id)
    result = list(Subcategory.objects.filter(category=target_category).values('id', 'name'))
    return HttpResponse(dumps(result), content_type='application/json')


def unsubscribe(request: HttpRequest) -> HttpResponse:
    """
    Если пользователь перешёл по ссылке для отписки, где в качестве GET-пара-
    метров передаётся хэш и сам email, то, если такой email существует в базе
    данных, удаляет его, иначе - сообщает об ошибке.
    """
    try:
        sub_email = EmailSubscription.objects.get(
            email_hash=request.GET['uid'],
            email=request.GET['email']
            )
        sub_email.delete()
        return render(request, 'blog/unsubscribe_success.html')
    except ObjectDoesNotExist:
        return render(request, 'blog/unsubscribe_failure.html')
