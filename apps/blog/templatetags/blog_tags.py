from typing import Any, Optional, Union
from django import template
from django.conf import settings
from django.utils.html import escape
from django.utils.safestring import SafeText, mark_safe
from django.conf import settings
from apps.manager.models import SiteSettings
from ..models import Article, Category, Subcategory, Status
from ..forms import SubscribeForm, FeedbackForm
from ..utils import get_word

register = template.Library()


@register.simple_tag
def get_categories() -> Category:
    """
    Возвращает все категории.
    """
    return Category.objects.all()


@register.simple_tag
def get_first_category_article(category: Category) -> str:
    """
    Возвращает первую статью в категории.
    """
    article = Article.objects.filter(
        category__name=category.name, 
        status=Status.PUBLISHED
    ).first()
    
    return article.get_absolute_url() if article else ''


@register.simple_tag
def get_next_and_prev_article(article: Article) -> str:
    """
    Возвращает следующую и предыдущую статьи.
    """
    subcategory_articles = Article.objects.filter(
        category=article.category, 
        status=Status.PUBLISHED
    )
    articles = [article['title'] for article in list(subcategory_articles.values('title'))]
    
    next_article, prev_article = None, None
    
    next_article_index = articles.index(article.title) + 1
    prev_article_index = articles.index(article.title) - 1
    
    if next_article_index < len(articles):
        next_article = subcategory_articles.get(title=articles[next_article_index])
        
    if prev_article_index > -1:
        prev_article = subcategory_articles.get(title=articles[prev_article_index])

    return {'next_article': next_article, 'prev_article': prev_article}


@register.simple_tag
def get_content_links(article: Article) -> dict:
    """
    Возвращает содержание категории в виде словаря, где ключи - подкатегории,
    значения - список статей подкатегории.
    """
    content_links = {} 
    
    if article.subcategory:
        subcategories = Subcategory.objects.filter(category=article.category)
        for subcategory in subcategories:
            content_links[subcategory] = Article.objects.filter(
                subcategory__name=subcategory,
                status=Status.PUBLISHED,
            )
        return content_links
    else:
        content_links = Article.objects.filter(
            category__name=article.category, 
            status=Status.PUBLISHED
        )

    return content_links


@register.filter
def cut_number(text: str) -> Union[SafeText, str]:
    """
    Обрезает первое слово в переданном тексте, если оно является числом.
    """
    if not settings.IS_CUT_NUMBER:
        return
    
    text_words = escape(text).split()
    
    if not len(text_words):
        return ''
    
    if not text_words[0][0].isdigit():
        return text
    
    text = ' '.join([word for word in text_words[1:]])

    return mark_safe(text)


@register.simple_tag
def get_comments_count(article: Article) -> int:
    """
    Возвращает количество комментариев к статье.
    """
    return article.comment_set.count()


@register.inclusion_tag('blog/includes/subscribe_form.html')
def subscribe_form(**kwargs: Any) -> dict:
    """
    Возвращает форму подписки на блог.
    """
    form = SubscribeForm()
    return {'subscribe_form': form}


@register.inclusion_tag('blog/includes/feedback_form.html')
def feedback_form(**kwargs: Any) -> dict:
    """
    Возвращает форму обратной связи.
    """
    form = FeedbackForm()
    return {'feedback_form': form}


@register.simple_tag
def get_results_word(n: int, i: int) -> str:
    """
    Возвращает склонения существительных во фразе о результатах поиска
    в зависимости от их количества.
    """
    ind = get_word(int(n))
    pairs = {0: ('найдено', 'результатов'),
             1: ('найден', 'результат'),
             2: ('найдено', 'результата')
             }
    return pairs[ind][i]


@register.simple_tag
def get_comments_word(n: int) -> str:
    """
    Возвращает склонение слова "комментарии" в зависимости от их количества.
    """
    ind = get_word(int(n))
    pairs = {0: 'комментариев',
             1: 'комментарий',
             2: 'комментария'
             }
    return pairs[ind]


@register.simple_tag
def get_search_results_count(article: Article) -> int:
    """
    Вовзвращает количество найденных статей.
    """
    return article.count()


@register.simple_tag
def get_site_settings() -> Optional[SiteSettings]:
    """
    Возвращает описание сайта.
    """
    return SiteSettings.objects.all().first()