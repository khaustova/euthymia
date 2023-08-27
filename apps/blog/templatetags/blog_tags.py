from django import template
from ..models import Article, Category, Tag
from ..forms import SubscribeForm, FeedbackForm

register = template.Library()

@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.simple_tag
def get_tags():
    return Tag.objects.all()


@register.simple_tag
def get_hot_articles():
    return Article.objects.all().order_by('-views')[:5]


@register.simple_tag
def get_comments_count(article):
    return article.comment_set.count()


@register.inclusion_tag('blog/includes/subscribe_form.html')
def subscribe_form(**kwargs):
    form = SubscribeForm()
    return {'subscribe_form' : form }


@register.inclusion_tag('blog/includes/feedback_form.html')
def feedback_form(**kwargs):
    form = FeedbackForm()
    return {'feedback_form' : form }


def get_word(n):
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
    ind = get_word(int(n))
    pairs = {0: ('найдено', 'результатов'), 
            1: ('найден', 'результат'),
            2: ('найдено', 'результата')}
    return pairs[ind][i]


@register.simple_tag
def get_comments_word(n):
    ind = get_word(int(n))
    pairs = {0: 'комментариев',
             1: 'комментарий',
             2: 'комментария'}
    return pairs[ind]

@register.simple_tag
def get_search_results_count(article):
    return article.count()

# @register.filter
# def highlight_search(text, search):
#     highlighted = text.replace(search, '<span class="highlight">{}</span>'.format(search))
#     return mark_safe(highlighted)