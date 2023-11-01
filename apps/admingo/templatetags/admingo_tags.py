import requests
import json

from copy import deepcopy
from typing import Optional

from django import template
from django.apps import apps
from django.urls import reverse
from django.http import HttpRequest
from django.utils.html import escape
from django.utils.safestring import SafeText, mark_safe
from django.utils.text import get_text_list
from django.utils.translation import gettext
from django.contrib.admin.models import LogEntry

from django.contrib.admin.templatetags.admin_list import result_list
from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.utils.html import format_html

from bs4 import BeautifulSoup

from core.settings import YANDEX_METRIKA_TOKEN, YANDEX_METRIKA_COUNTER
from ..settings import get_settings
from ..utils import order_items
from ..models import Notification

register = template.Library()


@register.simple_tag
def sidebar_status(request: HttpRequest) -> str:
    """
    Если у пользователя боковая панель свёрнута, то возвращает
    соответствующий CSS класс.
    """
    if request.COOKIES.get('menu', '') == 'closed':
        return 'sidebar-collapse'

    return


@register.simple_tag
def get_customization_settings() -> dict:
    """
    Возвращает словарь с настройками кастомизации панели администратора.
    """
    customization_settings = get_settings()

    return customization_settings


@register.simple_tag
def get_search_model() -> dict:
    """
    Возвращает словарь с параметрами для поиска по модели.
    """
    settings = get_settings()

    if not settings['search_model']:
        return

    search_model = settings['search_model']
    search_model_params = {}
    search_app_name, search_model_name = search_model.split('.')
    search_model_params['search_url'] = reverse(f'admin:{search_app_name}_{search_model_name}_changelist')
    search_model_meta = apps.get_registered_model(search_app_name, search_model_name)._meta
    search_model_params['search_name'] = search_model_meta.verbose_name_plural.title()

    return search_model_params


@register.simple_tag(takes_context=True)
def get_apps(context: template.Context) -> list:
    """
    Возвращает список приложений, отфильтрованный и упорядоченный в соответ-
    ствии с настройками кастомизации.
    """
    available_apps = deepcopy(context.get('available_apps', []))
    settings = get_settings()
    sidebar_icons = settings['sidebar_icons']
    apps_order = settings.get('apps_order', [])
    apps_order = [app.lower() for app in apps_order]
    apps = []

    for app in available_apps:
        app_label = app['app_label']
        if app_label in settings['hidden_apps']:
            continue
        models = []
        for model in app.get('models', []):
            model_name = f'{app_label}.{model["object_name"]}'.lower()
            if model_name in settings['hidden_models']:
                continue
            model['icon'] = sidebar_icons.get(model_name, 'circle')
            models.append(model)

        models_reference = list(filter(lambda app: '.' in app, apps_order))
        if models_reference:
            models = order_items(
                models,
                models_reference,
                getter=lambda app: app_label
                + '.'
                + app.get('object_name').lower()
            )
        app['models'] = models
        apps.append(app)

    if apps_order:
        apps_reference = list(filter(lambda app: '.' not in app, apps_order))
        apps = order_items(
            apps,
            apps_reference,
            getter=lambda app: app['app_label'].lower()
        )

    return apps


@register.simple_tag(takes_context=True)
def get_sidebar_menu(context: template.Context) -> list:
    """
    Возвращает список приложений, включающий в себя (при наличии) дополнитель-
    ные ссылки, для меню на боковой панели.
    """
    menu = get_apps(context)
    settings = get_settings()
    extra_links = settings.get('extra_links')

    if extra_links:
        for links_group in extra_links:
            for links_label, links in links_group.items():
                for app in menu:
                    app_label = app['app_label']
                    if links_label == app_label:
                        app['models'].extend(links)

    return menu


@register.simple_tag
def action_message_to_list(action: LogEntry) -> list:
    """
    Возвращает отформатированный список со всеми действиями пользователя.
    """
    messages = []

    if action.change_message and action.change_message[0] == '[':
        try:
            change_message = json.loads(action.change_message)
        except json.JSONDecodeError:
            return [action.change_message]

        for sub_message in change_message:
            if 'added' in sub_message:
                if sub_message['added']:
                    sub_message['added']['name'] = gettext(
                        sub_message['added']['name']
                    )
                    messages.append(
                        {
                            'message': (gettext('Added {name} «{object}».').format(**sub_message['added']))
                        }
                    )
                else:
                    messages.append({'message': (gettext('Added.'))})

            elif 'changed' in sub_message:
                sub_message['changed']['fields'] = get_text_list(
                    [
                        gettext(field_name) for field_name in sub_message['changed']['fields']
                    ], 
                    gettext('and'),
                )
                if 'name' in sub_message['changed']:
                    sub_message['changed']['name'] = gettext(
                        sub_message['changed']['name']
                    )
                    messages.append(
                        {
                            'message': (gettext('Changed {fields}.').format(**sub_message['changed']))
                        }
                    )
                else:
                    messages.append(
                        {
                            'message': (gettext('Changed {fields}.').format(**sub_message['changed']))
                        }
                    )

            elif 'deleted' in sub_message:
                sub_message['deleted']['name'] = gettext(sub_message['deleted']['name'])
                messages.append(
                    {
                        'message': (gettext('Deleted «{object}».').format(**sub_message['deleted']))
                    }
                )

    return messages if len(messages) else [
        {
            'message': (gettext(action.change_message))
        }
    ]


@register.filter
def bold_first_word(text: str) -> SafeText:
    """
    Возвращает текст, в котором первое слово обернуто в тег <strong>.
    """
    text_words = escape(text).split()

    if not len(text_words):
        return ''

    text_words[0] = '<strong>{}</strong>'.format(text_words[0])
    text = ' '.join([word for word in text_words])

    return mark_safe(text)


@register.simple_tag
def sort_header(header: dict, forloop: dict) -> str:
    """
    Вовзращает классы CSS для сортировки данных в столбцах таблицы модели.
    """
    classes = []
    sorted, asc, desc = (
        header.get('sorted'),
        header.get('ascending'),
        header.get('descending'),
    )

    is_checkbox_column_conditions = (
        forloop['counter0'] == 0,
        header.get('class_attrib') == ' class="action-checkbox-column"',
    )

    if all(is_checkbox_column_conditions):
        classes.append('djn-checkbox-select-all')

    if not header['sortable']:
        return ' '.join(classes)

    if sorted and asc:
        classes.append('sorting_asc')
    elif sorted and desc:
        classes.append('sorting_desc')
    else:
        classes.append('sorting')

    return ' '.join(classes)


@register.simple_tag()
def get_metrics() -> Optional[dict]:
    """
    Возвращает количество посителей и просмотров за день, неделю и месяц,
    полученное из Яндекс Метрики.
    """
    if YANDEX_METRIKA_COUNTER == 'counter':
        return
    
    API_URL = 'https://api-metrika.yandex.ru/stat/v1/data/bytime'
    params = {
        'date1': '30daysAgo',
        'date2': 'today',
        'metrics': 'ym:s:hits,ym:s:users',
        'group': 'day',
        'filters': "ym:s:isRobot=='No'",
        'id': YANDEX_METRIKA_COUNTER,
    }
    req = requests.get(
        API_URL, params=params, headers={
            'Authorization': YANDEX_METRIKA_TOKEN
        }
    )
    json_data = json.loads(req.text)

    results = {}
    results['today'] = {
        'views': int(json_data['totals'][0][-1]),
        'guests': int(json_data['totals'][1][-1])
    }
    results['week'] = {
        'views': int(sum(json_data['totals'][0][-7:])),
        'guests': int(sum(json_data['totals'][1][-7:])),
    }
    results['month'] = {
        'views': int(sum(json_data['totals'][0])),
        'guests': int(sum(json_data['totals'][1])),
    }

    return results


@register.simple_tag
def get_notifications_message(list: list) -> SafeText:
    """
    Вовзращает сообщение из уведомления.
    """
    message = list[2]
    soup = BeautifulSoup(message, 'lxml')
    notification = soup.find('td')

    return format_html(notification.text)


@register.simple_tag
def get_notifications_status(notification: Notification) -> bool:
    """
    Возвращает статус уведомления, как прочитанное или непрочитанное.
    """
    field_read = notification[-1].split()

    if field_read[-1].startswith('alt="False"'):
        return False
    return True


@register.tag(name="notifications_result_list")
def notifications_result_list_tag(parser, token):
    """
    Возвращает шаблон для страницы с уведомлениями.
    """
    return InclusionAdminNode(
        parser,
        token,
        func=result_list,
        template_name="change_list_notifications.html",
        takes_context=False,
    )


@register.simple_tag
def get_notifications() -> int:
    """
    Возвращает количество непрочитанных уведомлений.
    """
    unread_notifications = Notification.objects.filter(read=False)

    return unread_notifications.count()
