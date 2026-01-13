import logging
from akismet import Akismet
from json import dumps
from typing import Any
from ipware import get_client_ip

from django.conf import settings
from django.contrib import messages
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import F, Prefetch
from django.http import (
    HttpRequest, 
    HttpResponse, 
    HttpResponseRedirect, 
    Http404
)
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View

from .models import Article, Comment, Category, Subcategory, Status
from .forms import CommentForm

# Создаём логгеры
logger = logging.getLogger('website')
comment_logger = logging.getLogger('website.comments')
security_logger = logging.getLogger('security')


class ArticleView(ListView):
    """Отображает список опубликованных статей по популярности или по дате."""
    
    model = Article
    template_name = 'website/index.html'
    context_object_name = 'articles'
    paginate_by = 10
    paginate_orphans = 5

    def get_queryset(self) -> list[Article]:
        """Возвращает список опубликованных статей по популярности или по дате."""
        sort = self.kwargs.get('sort')

        if sort == 'views':
            logger.debug(f'Загрузка статей, отсортированных по просмотрам')
            return Article.objects.filter(
                status=Status.PUBLISHED
            ).order_by('-views', 'created_date')
        
        logger.debug(f'Загрузка статей, отсортированных по дате')
        return Article.objects.filter(
            status=Status.PUBLISHED
        ).order_by('-created_date')


class ArticleDetailView(DetailView):
    """Отображает информацию о статье."""
    
    model = Article
    template_name = 'website/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self) -> Article:
        """Оптимизация запросов к БД"""
        return Article.objects.select_related(
            'category', 
            'subcategory'
        ).prefetch_related(
            Prefetch(
                'comment_set',
                queryset=Comment.objects.select_related('author')
            )
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Добавляет в контекст данные о комментариях к статье, их количестве 
        и форме для отправки комментариев.
        """
        context = super().get_context_data(**kwargs)
        comments = self.object.comment_set.all()
        context['comments'] = comments
        context['comments_number'] = comments.count()
        context['form'] = CommentForm()
        
        logger.debug(
            f'Статья "{self.object.title}" (ID: {self.object.pk}) просмотрена. '
            f'Комментариев: {context["comments_number"]}'
        )
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseRedirect:
        """Обрабатывает отправку комментариев."""
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)
        
        # Получаем IP для логирования
        client_ip, is_routable = get_client_ip(request)
        user_ip = client_ip if client_ip else 'Unknown'
        
        if not comment_form.is_valid():
            comment_logger.warning(
                f'Невалидная форма комментария для статьи "{self.object.title}" '
                f'от IP {user_ip}. Ошибки: {comment_form.errors}'
            )
            context = self.get_context_data()
            context['form'] = comment_form
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            return self.render_to_response(context)
        
        try:
            new_comment = comment_form.save(commit=False)
            new_comment.article = self.object
            
            # Установка автора
            if request.user.is_authenticated:
                new_comment.author = request.user
                new_comment.email = request.user.email
                author_info = f"Пользователь: {request.user.username}"
            else:
                new_comment.guest = comment_form.cleaned_data.get('guest') or 'Безымянный'
                new_comment.email = comment_form.cleaned_data.get('email')
                author_info = f"Гость: {new_comment.guest}"
            
            # Установка IP-адреса
            if client_ip is None:
                new_comment.comment_ip = 'Unable'
            elif is_routable:
                new_comment.comment_ip = client_ip
            else:
                new_comment.comment_ip = 'Private'
            
            # Проверка на спам с помощью Akismet
            if settings.IS_USE_AKISMET:
                try:
                    akismet_api = Akismet(
                        key=settings.AKISMET_API_KEY, 
                        blog_url=settings.AKISMET_URL
                    )
                    
                    comment_author = (
                        request.user.username if request.user.is_authenticated 
                        else new_comment.guest
                    )
                    
                    is_spam = akismet_api.comment_check(
                        user_ip=new_comment.comment_ip,
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        comment_type='comment',
                        comment_author=comment_author,
                        comment_author_email=new_comment.email,
                        comment_content=comment_form.cleaned_data.get('body'),
                    )

                    if is_spam:
                        security_logger.warning(
                            f'ОБНАРУЖЕН СПАМ. Заблокирован комментарий к статье "{self.object.title}". '
                            f'{author_info}, IP: {new_comment.comment_ip}, '
                            f'Email: {new_comment.email}'
                        )
                        messages.error(
                            request,
                            'Ваш комментарий был отмечен как спам и не может быть опубликован.'
                        )
                        return redirect(request.path_info + '#comments')
                    
                    comment_logger.debug(
                        f'Проверка Akismet пройдена для комментария к "{self.object.title}"'
                    )
                    
                except Exception as e:
                    logger.error(
                        f'Ошибка API Akismet для статьи "{self.object.title}": {e}',
                        exc_info=True
                    )
                    messages.warning(
                        request,
                        'Не удалось проверить комментарий на спам. '
                        'Комментарий будет опубликован.'
                    )

            # Сохраняем комментарий
            new_comment.save()
            
            comment_logger.info(
                f'Новый комментарий к статье "{self.object.title}" (ID: {self.object.pk}). '
                f'{author_info}, IP: {new_comment.comment_ip}, '
                f'ID комментария: {new_comment.pk}'
            )
            
            messages.success(request, 'Ваш комментарий успешно добавлен!')
            return redirect(request.path_info + '#comments')
            
        except Exception as e:
            logger.error(
                f'Ошибка сохранения комментария для статьи "{self.object.title}": {e}',
                exc_info=True
            )
            messages.error(
                request,
                'Произошла ошибка при сохранении комментария. Попробуйте позже.'
            )
            return redirect(request.path_info + '#comments')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Обрабатывает GET-запрос и увеличивает счётчик просмотров."""
        response = super().get(request, *args, **kwargs)
        
        # Увеличение счётчика просмотров только один раз за сессию
        session_key = f'viewed_article_{self.object.pk}'
        if not request.session.get(session_key):
            Article.objects.filter(pk=self.object.pk).update(views=F('views') + 1)
            request.session[session_key] = True
            
            logger.debug(
                f'Увеличен счётчик просмотров статьи "{self.object.title}" '
                f'(ID: {self.object.pk})'
            )
        
        return response


class CategoryRedirectView(View):
    """Находит первую статью в указанной категории и перенаправляет на нее."""
    
    def get(self, request: HttpRequest, category: str) -> HttpResponseRedirect:
        logger.debug(f'Поиск первой статьи в категории: {category}')
        
        first_article = Article.objects.filter(
            category__slug=category,
            status=Status.PUBLISHED
        ).order_by('main_number', 'sub_number').first()
        
        if first_article:
            logger.info(
                f'Перенаправление на первую статью "{first_article.title}" '
                f'в категории "{category}"'
            )
            return redirect('website:article_detail', category, first_article.slug)
        else:
            logger.warning(f'Не найдено опубликованных статей в категории: {category}')
            raise Http404('В этой категории нет статей.')


class SearchView(ListView):
    """Отображает список опубликованных статей в соответствии с запросом."""
    
    model = Article
    context_object_name = 'articles'
    template_name = 'website/search_results.html'
    paginate_by = 10
    paginate_orphans = 5

    def get_queryset(self) -> list[Article]:
        """
        Возвращает список статей в соответствии с запросом.
        """
        query = self.request.GET.get('query', '').strip()
        
        if not query:
            logger.info('Получен пустой поисковый запрос')
            return Article.objects.none()
        
        logger.info(f'Поиск статей по запросу: "{query}"')
        
        search_vector = SearchVector('title', 'body')
        search_query = SearchQuery(query)
        
        results = (
            Article.objects.annotate(
                search=search_vector, 
                rank=SearchRank(search_vector, search_query)
            )
            .filter(search=search_query, status=Status.PUBLISHED)
            .order_by('-rank')
        )
        
        logger.info(f'Поисковый запрос "{query}" вернул {results.count()} результатов')
        return results

def get_subcategory(request: HttpRequest) -> HttpResponse:
    """В формате JSON возвращает только те подкатегории, что принадлежат 
    выбранной категории. Используется при создании статьи.
    """
    if request.method != 'GET':
        logger.warning(f'Недопустимый метод {request.method} для get_subcategory')
        return HttpResponse(
            dumps({'error': 'Method not allowed'}),
            content_type='application/json',
            status=405
        )
    
    category_id = request.GET.get('id', '').strip()
    
    if not category_id:
        logger.warning('get_subcategory вызван без ID категории')
        return HttpResponse(
            dumps({'error': 'ID категории не указан'}),
            content_type='application/json',
            status=400
        )
    
    try:
        target_category = Category.objects.get(pk=category_id)
        result = list(
            Subcategory.objects.filter(category=target_category)
            .values('id', 'name')
        )
        
        logger.debug(
            f'Получено {len(result)} подкатегорий для категории "{target_category.name}"'
        )
        
        return HttpResponse(dumps(result), content_type='application/json')
        
    except Category.DoesNotExist:
        logger.warning(f'Категория с ID {category_id} не найдена')
        return HttpResponse(
            dumps({'error': 'Категория не найдена'}),
            content_type='application/json',
            status=404
        )
    except Exception as e:
        logger.error(
            f'Ошибка получения подкатегорий для категории с ID {category_id}: {e}',
            exc_info=True
        )
        return HttpResponse(
            dumps({'error': 'Внутренняя ошибка сервера'}),
            content_type='application/json',
            status=500
        )
