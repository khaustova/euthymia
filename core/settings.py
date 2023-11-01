from pathlib import Path
from sys import path
from environ import Env


BASE_DIR = Path(__file__).resolve().parent.parent
path.append(str(BASE_DIR / 'apps'))

env = Env(
    DEBUG=(bool, False)
)
Env.read_env(BASE_DIR / '.env.example')

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS').split(' ')

LOGIN_REDIRECT_URL = '/'

CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS').split(' ')

INTERNAL_IPS = env('INTERNAL_IPS').split(' ')

# Application definition

INSTALLED_APPS = [
    'admingo',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'debug_toolbar',
    'ckeditor',
    'ckeditor_uploader',
    'admin_auto_filters',
    'imagekit',
    'mptt',
    'django_celery_results',
    'blog',
    'manager',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database

DATABASES = {
    "default": {
        "ENGINE": env("POSTGRES_ENGINE"),
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# Media files

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKEDITOR config

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moonocolor',
        'width': '100%',
        'toolbar': [
            {
                'name': 'document',
                'items': [
                    'Source',
                    '-',
                    'Save',
                    'Preview',
                    '-',
                ]
            },
            {
                'name': 'clipboard',
                'items': [
                    'Paste',
                    'PasteText',
                    'PasteFromWord',
                    '-',
                    'Undo',
                    'Redo',
                ]
            },
            {
                'name': 'editing',
                'items': [
                    'Find', 'Replace',
                ]
            },
            '/',
            {
                'name': 'basicstyles',
                'items': [
                    'Bold',
                    'Italic',
                    'Underline',
                    'Strike',
                    'Subscript',
                    'Superscript',
                    '-',
                    'RemoveFormat',
                ]
            },
            {
                'name': 'paragraph',
                'items': [
                    'NumberedList',
                    'BulletedList',
                    '-',
                    'Outdent',
                    'Indent',
                    '-',
                    'Blockquote',
                    '-',
                    'JustifyLeft',
                    'JustifyCenter',
                    'JustifyRight',
                    'JustifyBlock',
                ]
            },
            {
                'name': 'links',
                'items': [
                    'Link',
                    'Unlink',
                    'Anchor',
                ]
            },
            {
                'name': 'insert',
                'items': [
                    'Image',
                    'Flash',
                    'Table',
                    'HorizontalRule',
                    'Smiley',
                    'SpecialChar',
                ]
            },
            '/',
            {
                'name': 'styles',
                'items': [
                    'Styles',
                    'Format',
                    'Font',
                    'FontSize',
                ]
            },
            {
                'name': 'colors',
                'items': [
                    'TextColor',
                    'BGColor',
                ]
            },
            {
                'name': 'tools',
                'items': [
                    'Maximize', 'ShowBlocks',
                ]
            },
            '/',
            {
                'name': 'yourcustomtools',
                'items': [
                    'Maximize',
                    'CodeSnippet',
                ]
            },
        ],
        'tabSpaces': 4,
        'codeSnippet_theme': 'tomorrow-night-blue',
        'extraPlugins': ','.join(
            [
                'codesnippet',
                'widget',
                'dialog',
                'stylescombo'
            ]
        ),
        'codeSnippet_languages': {
            'python': 'Python',
        },
        'stylesSet': [
            {
                'name': 'Строчный код', 
                'element': 'code'
            },
            {
                'name': 'Монолитный элемент', 
                'element': 'span', 
                'attributes': {
                    'style': 'white-space: nowrap;'
                }
            },
            {
                'name': 'Адаптивный блок', 
                'element': 'div', 
                'attributes': {
                    'class': 'responsive-block'
                }
            }
        ],
    }
}

# Email

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

# Celery

CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_ACCEPT_CONTENT = {'application/json'}
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Analytics

YANDEX_METRIKA_TOKEN = env('YANDEX_METRIKA_TOKEN')
YANDEX_METRIKA_COUNTER = env('YANDEX_METRIKA_COUNTER')

# Admingo

ADMINGO_CUSTOMIZATION = {
    'search_model': 'blog.article',
    'sidebar_icons': {
        'auth.user': 'person',
        'auth.group': 'groups',
        'blog.article': 'article',
        'blog.tag': 'bookmark',
        'blog.category': 'category',
        'blog.comment': 'chat',
        'manager.feedback': 'rate_review',
        'manager.emailsubscription': 'email',
        'manager.sitedescription': 'settings',
        'django_celery_results.taskresult': 'task',
    },
    'hidden_apps': [
        'admingo',
    ],
    'hidden_models': [
        'auth.group',
        'django_celery_results.groupresult',
    ],
    'apps_order': [
        'blog',
        'blog.article',
        'blog.tag',
        'blog.category',
        'manager',
        'manager.feedback',
        'manager.emailsubscription',
        'manager.sitedescription',
        'django_celery_results',
        'auth',
    ],
    'extra_links': [
        {
            'manager': [
                {
                    'name': 'Документация',
                    'admin_url': '/admin/doc/',
                    'icon': 'description'
                },
                {
                    'name': 'Яндекс Метрика',
                    'admin_url': 'https://metrika.yandex.ru/dashboard?group=day&period=week&id='
                        + YANDEX_METRIKA_COUNTER,
                    'icon': 'monitoring'
                }
            ]
        }
    ],
}

# Обрезается ли номер в заголовке статьи

IS_CUT_NUMBER = True

# Защита от спама с помощью Akismet 

IS_USE_AKISMET = False
AKISMET_API_KEY = env('AKISMET_API_KEY')
AKISMET_BLOG_URL = env('AKISMET_BLOG_URL')