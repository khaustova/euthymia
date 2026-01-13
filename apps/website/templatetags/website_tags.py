import logging
from typing import Optional, Union
from django import template
from django.conf import settings
from django.core.cache import cache
from django.db.models import Prefetch, Q
from django.utils.html import escape
from django.utils.safestring import SafeText, mark_safe

from apps.website.models import SiteSettings
from ..models import Article, Category, Subcategory, Status, Type
from ..utils import get_declension_code

register = template.Library()
logger = logging.getLogger('website')

CACHE_TIMEOUT_SHORT = 300      # 5 минут
CACHE_TIMEOUT_MEDIUM = 1800    # 30 минут
CACHE_TIMEOUT_LONG = 3600      # 1 час
CACHE_TIMEOUT_VERY_LONG = 86400  # 24 часа


@register.simple_tag
def get_textbook_categories() -> list[Category]:
    """Возвращает все категории учебников с кэшированием.
    Кэш: 1 час.
    """
    cache_key = 'textbook_categories'
    categories = cache.get(cache_key)
    
    if categories is None:
        categories = list(
            Category.objects.filter(type=Type.ТEXTBOOK).order_by('name')
        )
        cache.set(cache_key, categories, CACHE_TIMEOUT_LONG)
        logger.debug(f'Категории учебников загружены из БД и закэшированы')
    
    return categories


@register.simple_tag
def get_projects_categories() -> list[Category]:
    """Возвращает все категории проектов."""
    cache_key = 'projects_categories'
    categories = cache.get(cache_key)
    
    if categories is None:
        categories = list(
            Category.objects.filter(type=Type.PROJECTS).order_by('name')
        )
        cache.set(cache_key, categories, CACHE_TIMEOUT_LONG)
        logger.debug(f'Категории проектов загружены из БД и закэшированы')
    
    return categories


@register.simple_tag
def get_first_category_article(category: Category) -> str:
    """Возвращает URL первой статьи в категории."""
    cache_key = f'first_article_category_{category.pk}'
    url = cache.get(cache_key)
    
    if url is None:
        article = Article.objects.filter(
            category=category,
            status=Status.PUBLISHED
        ).order_by('main_number', 'sub_number').first()
        
        url = article.get_absolute_url() if article else ''
        cache.set(cache_key, url, CACHE_TIMEOUT_MEDIUM)
        logger.debug(f'Первая статья категории "{category.name}" закэширована')
    
    return url


@register.simple_tag
def get_next_and_prev_article(article: Article) -> dict[str, Optional[Article]]:
    """Возвращает следующую и предыдущую статьи."""
    cache_key = f'nav_articles_{article.pk}'
    result = cache.get(cache_key)
    
    if result is None:
        next_article = Article.objects.filter(
            category=article.category,
            status=Status.PUBLISHED
        ).filter(
            Q(main_number=article.main_number, sub_number__gt=article.sub_number) |
            Q(main_number__gt=article.main_number)
        ).order_by('main_number', 'sub_number').first()
        
        prev_article = Article.objects.filter(
            category=article.category,
            status=Status.PUBLISHED
        ).filter(
            Q(main_number=article.main_number, sub_number__lt=article.sub_number) |
            Q(main_number__lt=article.main_number)
        ).order_by('-main_number', '-sub_number').first()
        
        result = {
            'next_article': next_article,
            'prev_article': prev_article
        }
        
        cache.set(cache_key, result, CACHE_TIMEOUT_MEDIUM)
        logger.debug(f'Навигация для статьи "{article.title}" закэширована')
    
    return result


@register.simple_tag
def get_content_links(article: Article) -> dict[Subcategory, list[Article]] | list[Article]:
    """Возвращает содержание категории.
    Если есть подкатегории - словарь {подкатегория: [статьи]},
    иначе - список статей.
    """
    cache_key = f'content_links_{article.category.pk}_{bool(article.subcategory)}'
    content_links = cache.get(cache_key)
    
    if content_links is None:
        try:
            if article.subcategory:
                # Есть подкатегории - группируем по ним
                subcategories = Subcategory.objects.filter(
                    category=article.category
                ).prefetch_related(
                    Prefetch(
                        'article_set',
                        queryset=Article.objects.filter(
                            status=Status.PUBLISHED
                        ).order_by('main_number', 'sub_number'),
                        to_attr='published_articles'
                    )
                ).order_by('name')
                
                # Создаём словарь без дополнительных запросов
                content_links = {
                    subcategory: subcategory.published_articles
                    for subcategory in subcategories
                }
            else:
                # Нет подкатегорий - просто список статей
                content_links = list(
                    Article.objects.filter(
                        category=article.category,
                        status=Status.PUBLISHED
                    ).order_by('main_number', 'sub_number')
                )
            
            cache.set(cache_key, content_links, CACHE_TIMEOUT_MEDIUM)
            logger.debug(f'Содержание категории "{article.category.name}" закэшировано')
        except Exception as e:
            logger.error(
                f'Ошибка получения содержания для статьи "{article.title}": {e}',
                exc_info=True
            )
            return {} if article.subcategory else []
    
    return content_links


@register.filter
def cut_number(text: str) -> Union[SafeText, str]:
    """Обрезает первое слово в переданном тексте, если оно является числом."""
    if not text:
        return ''
    
    # Если настройка отключена, возвращаем исходный текст
    if not settings.IS_CUT_NUMBER:
        return text

    text_words = escape(text).split()
    
    if not text_words:
        return ''
    
    # Проверяем, начинается ли первое слово с цифры
    if not text_words[0][0].isdigit():
        return text
    
    # Убираем первое слово
    text = ' '.join(text_words[1:])
    
    return mark_safe(text)


@register.filter
def cut_text(text: str) -> Union[SafeText, str]:
    """Возвращает первое слово из текста."""
    if not text:
        return ''
    
    text_words = escape(text).split()
    
    if not text_words:
        return ''
    
    return mark_safe(text_words[0])



@register.simple_tag
def get_comments_count(article: Article) -> int:
    """Возвращает количество комментариев к статье."""
    try:
        return article.comment_set.count()
    except Exception as e:
        logger.error(
            f'Ошибка подсчёта комментариев для статьи "{article.title}": {e}',
            exc_info=True
        )
        return 0


@register.simple_tag
def get_results_word(n: int, i: int) -> str:
    """Возвращает склонения существительных во фразе о результатах поиска
    в зависимости от их количества.
    
    Args:
        n: количество результатов
        i: индекс слова (0 - глагол, 1 - существительное)
    
    Returns:
        Правильная форма слова
    """
    ind = get_declension_code(int(n))
    pairs = {
        0: ('найдено', 'статей'),
        1: ('найдена', 'статья'),
        2: ('найдено', 'статьи')
    }
    return pairs[ind][i]


@register.simple_tag
def get_comments_word(n: int) -> str:
    """Возвращает склонение слова "комментарий" в зависимости от количества.
    
    Args:
        n: количество комментариев
    
    Returns:
        Правильная форма слова "комментарий"
    """
    ind = get_declension_code(int(n))
    pairs = {
        0: 'комментариев',
        1: 'комментарий',
        2: 'комментария'
    }
    return pairs[ind]


@register.simple_tag
def get_search_results_count(articles) -> int:
    """Возвращает количество найденных статей.
    
    Args:
        articles: QuerySet или список статей
    
    Returns:
        Количество статей
    """
    if hasattr(articles, 'count'):
        return articles.count()
    return len(articles)


@register.simple_tag
def get_site_settings() -> Optional[SiteSettings]:
    """Возвращает настройки сайта."""
    cache_key = 'site_settings'
    settings_obj = cache.get(cache_key)
    
    if settings_obj is None:
        settings_obj = SiteSettings.objects.first()
        # Кэшируем на 24 часа
        cache.set(cache_key, settings_obj, CACHE_TIMEOUT_VERY_LONG)
        logger.debug('Настройки сайта загружены из БД и закэшированы')
    
    return settings_obj


@register.simple_tag
def get_site_description() -> str:
    """Возвращает описание сайта."""
    settings = get_site_settings()
    return settings.site_description if settings else ''


@register.simple_tag
def get_about_me() -> str:
    """Возвращает информацию об авторе."""
    settings = get_site_settings()
    return settings.about_me if settings else ''
