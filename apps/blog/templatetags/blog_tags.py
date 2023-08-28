from django import template
from django.utils.html import escape
from django.utils.safestring import SafeText, mark_safe
from ..models import Article, Category, Tag
from ..forms import SubscribeForm, FeedbackForm

register = template.Library()


@register.simple_tag
def get_categories():
    """
    Возвращает все категории.
    """
    return Category.objects.all()


@register.simple_tag
def get_first_article(category):
    subcategories = [cat.name for cat in category.get_children()]
    article = Article.objects.filter(category__name__in=subcategories).first()
    article_url = article.get_absolute_url()
    return article_url 


@register.simple_tag
def get_content_links(article):
    subcategory = article.category
    content_links = {}
    subcategories = [ cat.name for cat in subcategory.get_siblings(include_self=True)]
    for subcategory in subcategories:
        content_links[subcategory] = Article.objects.filter(category__name=subcategory)
    return content_links


@register.simple_tag
def get_category(article):
    """
    Возвращает все теги.
    """
    return article.category.get_root()

@register.filter
def cut_number(text: str) -> SafeText:
    text_words = escape(text).split()
    
    if not len(text_words):
        return ''

    text = ' '.join([word for word in text_words[1:]])
    
    return mark_safe(text)


@register.simple_tag
def get_tags():
    """
    Возвращает все теги.
    """
    return Tag.objects.all()


@register.simple_tag
def get_comments_count(article):
    """
    Возвращает количество комментариев к статье.
    """
    return article.comment_set.count()


@register.inclusion_tag('blog/includes/subscribe_form.html')
def subscribe_form(**kwargs):
    """
    Возвращает форму подписки на блог.
    """
    form = SubscribeForm()
    return {'subscribe_form' : form }


@register.inclusion_tag('blog/includes/feedback_form.html')
def feedback_form(**kwargs):
    """
    Возвращает форму обратной связи.
    """
    form = FeedbackForm()
    return {'feedback_form' : form }


def get_word(n):
    """
    Возвращает группу склонения существительного после числительного.
    """
    n %= 100
    if n >= 5 and n <= 20:
        return 0
    n %= 10;
    if n == 1:
        return 1
    elif n >= 2 and n <= 4:
        return 2
    return 0

@register.simple_tag
def get_results_word(n, i):
    """
    Возвращает склонения существительных во фразе о результатах поиска
    в зависимости от их количества.
    """
    ind = get_word(int(n))
    pairs = {0: ('найдено', 'результатов'), 
            1: ('найден', 'результат'),
            2: ('найдено', 'результата')}
    return pairs[ind][i]


@register.simple_tag
def get_comments_word(n):
    """
    Возвращает склонение слова "комментарии" в зависимости от их количества
    """
    ind = get_word(int(n))
    pairs = {0: 'комментариев',
             1: 'комментарий',
             2: 'комментария'}
    return pairs[ind]


@register.simple_tag
def get_search_results_count(article):
    """
    Вовзвращает количество найденных статей.
    """
    return article.count()
