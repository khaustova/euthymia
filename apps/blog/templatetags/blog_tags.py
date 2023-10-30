from typing import Any, Optional, Union
from django import template
from django.utils.html import escape
from django.utils.safestring import SafeText, mark_safe
from django.conf import settings
from manager.models import SiteDescription
from ..models import Article, Category, Subcategory
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
    article = Article.objects.filter(category__name=category.name).first()
    
    return article.get_absolute_url()


@register.simple_tag
def get_next_and_prev_article(article: Article) -> str:
    """
    Возвращает следующую и предыдущую статьи.
    """
    subcategory_articles = Article.objects.filter(category=article.category)
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
    subcategory = article.subcategory
    subcategories = Subcategory.objects.filter(category=article.category)

    content_links = {} 
    for subcategory in subcategories:
        content_links[subcategory] = Article.objects.filter(
            subcategory__name=subcategory
        )

    return content_links


@register.filter
def cut_number(text: str) -> Union[SafeText, str]:
    """
    Обрезает номер в заголовке статьи.
    """
    if not settings.IS_CUT_NUMBER:
        return
    
    text_words = escape(text).split()

    if not len(text_words):
        return ''

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
    Возвращает склонение слова "комментарии" в зависимости от их количества
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
def get_site_description() -> Optional[SiteDescription]:
    """
    Возвращает описание сайта.
    """
    return SiteDescription.objects.all().first()
