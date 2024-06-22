from pathlib import Path
from environ import Env


BASE_DIR = Path(__file__).resolve().parent.parent

env = Env(
    DEBUG=(bool, False),
    IS_USE_AKISMET=(bool, False)
)
Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS').split(' ')

LOGIN_REDIRECT_URL = '/'

CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS').split(' ')

INTERNAL_IPS = env('INTERNAL_IPS').split(' ')

# Application definition

INSTALLED_APPS = [
    'apps.dashboard.apps.DashboardConfig',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'debug_toolbar',
    'ckeditor',
    'ckeditor_uploader',
    'admin_auto_filters',
    'mptt',
    'django_celery_results',
    'apps.blog.apps.BlogConfig',
    'apps.manager.apps.ManagerConfig',
]

SITE_ID = 1

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
    'default': {
        'ENGINE': env('POSTGRES_ENGINE'),
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
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

# Logs

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)-12s %(message)s'
        },
    },
    'handlers': {
        'logit': {
            'level': env('LOG_LEVEL'),
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(BASE_DIR / 'django.log'),
            'maxBytes': 15728640,  # 1024 * 1024 * 15B = 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.server': {
            'handlers': ['logit'],
            'level': env('LOG_LEVEL'),
            'propagate': True,
        },
    },
}

# CKEDITOR config

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moonocolor',
        'width': '100%',
        'contentsCss': '/static/dashboard/css/editor.css',
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
                    'CodeSnippet',
                    'Spoiler',
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
        ],
        'tabSpaces': 4,
        'codeSnippet_theme': 'tomorrow-night-blue',
        'extraPlugins': ','.join(
            [
                'codesnippet',
                'widget',
                'dialog',
                'stylescombo',
                'spoiler'
            ]
        ),
        'codeSnippet_languages': {
            'python': 'Python',
            'C': 'C',
            'bash': 'Bash',
            'xml': 'XML',
            'javascript': 'JavaScript'
        },
        'stylesSet': [
            {
                'name': 'Адаптивный блок', 
                'element': 'div', 
                'attributes': {
                    'class': 'responsive-block'
                }
            },
            {
                'name': 'Примеры данных', 
                'element': 'div', 
                'attributes': {
                    'class': 'responsive-data-block'
                }
            },
            {
                'name': 'Разделитель', 
                'element': 'div', 
                'attributes': {
                    'class': 'separator'
                }
            },
            {
                'name': 'Дополнительная информация', 
                'element': 'p', 
                'attributes': {
                    'class': 'extra-info'
                }
            },
            {
                'name': 'Внимание!', 
                'element': 'div', 
                'attributes': {
                    'class': 'warning-info'
                }
            },
            {
                'name': 'Код в тексте',
                'element': 'span',
                'attributes': {
                    'class': 'code'
                }
            }, 
            {
                'name': 'Figure', 
                'element': 'figure', 
            },  
            {
                'name': 'Figcaption', 
                'element': 'figcaption', 
            },
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

# Dashboard

DASHBOARD_CUSTOMIZATION = {
    'search_model': 'blog.article',
    'sidebar_icons': {
        'auth.user': 'person',
        'auth.group': 'groups',
        'blog.article': 'article',
        'blog.category': 'category',
        'blog.subcategory': 'bookmark',
        'blog.comment': 'chat_bubble',
        'manager.feedback': 'rate_review',
        'manager.emailsubscription': 'email',
        'manager.sitesettings': 'settings',
        'django_celery_results.taskresult': 'task',
    },
    'hidden_apps': [
        'dashboard',
        'sites',
    ],
    'hidden_models': [
        'auth.group',
        'django_celery_results.groupresult',
    ],
    'apps_order': [
        'blog',
        'blog.article',
        'blog.comment',
        'blog.category',
        'blog.subcategory',
        'manager',
        'manager.feedback',
        'manager.emailsubscription',
        'manager.sitesettings',
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
                },
                {
                    'name': 'Сайты',
                    'admin_url': '/admin/sites/site/',
                    'icon': 'web'
                },
            ]
        }
    ],
}

# Обрезается ли номер в заголовке статьи

IS_CUT_NUMBER = True

# Защита от спама с помощью Akismet 

IS_USE_AKISMET = env('IS_USE_AKISMET')
AKISMET_API_KEY = env('AKISMET_API_KEY')
AKISMET_BLOG_URL = env('AKISMET_BLOG_URL')
