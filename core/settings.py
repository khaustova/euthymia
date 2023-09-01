"""
Django settings for core project.
"""

from pathlib import Path
from environ import Env
from sys import path

BASE_DIR = Path(__file__).resolve().parent.parent
path.append(str(BASE_DIR / 'apps'))

env = Env(
    DEBUG=(bool, False)
)
Env.read_env(BASE_DIR / '.env.example')

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(' ')

LOGIN_REDIRECT_URL = '/'

# Application definition

INSTALLED_APPS = [
    'admingo.apps.AdmingoConfig',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'imagekit',
    'mptt',
    'blog.apps.BlogConfig',
    'manager.apps.ManagerConfig',
    'django_elasticsearch_dsl',
    'django_celery_results',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware'
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
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

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
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
CKEDITOR_UPLOAD_PATH = "uploads/"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

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
            {'name': 'document', 'items': ['Source', '-', 'Save', 'Preview', '-',]
             },
            {'name': 'clipboard', 'items': ['Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']
             },
            {'name': 'editing', 'items': ['Find', 'Replace',]
             },
            '/',
            {'name': 'basicstyles','items':  ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 
                                              'Superscript', '-', 'RemoveFormat']
             },
            {'name': 'paragraph', 'items':  ['NumberedList', 'BulletedList', '-', 
                                             'Outdent', 'Indent', '-',  'Blockquote', 
                                             '-', 'JustifyLeft', 'JustifyCenter', 
                                             'JustifyRight', 'JustifyBlock']
              },
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']
             },
            {'name': 'insert','items': ['Image', 'Flash', 'Table', 'HorizontalRule', 
                                        'Smiley', 'SpecialChar']
            },
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']
             },
            {'name': 'colors', 'items': ['TextColor', 'BGColor']
             },
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']
             },
            '/', 
            {'name': 'yourcustomtools', 'items': ['Maximize', 'CodeSnippet',]
             },
        ],
        'tabSpaces': 4,
        'codeSnippet_theme': 'tomorrow-night-blue',
        'extraPlugins': ','.join([
            'codesnippet',
            'widget',
            'dialog',
        ]),
        'codeSnippet_languages': {
            'python': 'Python',
        },
    }
}

# Elasticsearch
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'elasticsearch:9200',
        'verify_certs': False,
        'ca_certs': None
    },
}

# Email
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')

EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'default from email'

# Celery
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_ACCEPT_CONTENT = {'application/json'}
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True

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
    'hidden_apps': ['admingo'],
    'hidden_models': ['auth.group', 'django_celery_results.groupresult'],
    'apps_order': ['blog', 'blog.article', 'blog.tag', 'blog.category', 
                   'manager', 'manager.feedback', 'manager.emailsubscription', 'manager.sitedescription',
                   'django_celery_results', 
                   'auth'],
    'extra_links' : [{'manager': [
                            {'name': 'Документация', 'admin_url': '/admin/doc/', 'icon': 'description'},
                        ]}
                     ],
}