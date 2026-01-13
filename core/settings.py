from pathlib import Path
from environ import Env

# ═══════════════════════════════════════════════════════════════════
# Общие настройки
# ═══════════════════════════════════════════════════════════════════

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
    'apps.website.apps.WebsiteConfig',
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

IS_CUT_NUMBER = True  # Обрезается ли номер в заголовке статьи

# ═══════════════════════════════════════════════════════════════════
# База данных
# ═══════════════════════════════════════════════════════════════════

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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ═══════════════════════════════════════════════════════════════════
# Язык и время
# ═══════════════════════════════════════════════════════════════════

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# ═══════════════════════════════════════════════════════════════════
# Работа с файлами
# ═══════════════════════════════════════════════════════════════════

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

if not DEBUG:
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ═══════════════════════════════════════════════════════════════════
# Логирование
# ═══════════════════════════════════════════════════════════════════

LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {module} {funcName} | {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[{levelname}] {asctime} | {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'detailed': {
            'format': '''
────────────────────────────────────────────────────
[{levelname}] {asctime}
Module: {module} | Function: {funcName}
Path: {pathname}:{lineno}
Message: {message}
────────────────────────────────────────────────────''',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'filters': ['require_debug_true'],
        },

        'file_all': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'all.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'errors.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'detailed',
            'encoding': 'utf-8',
        },
        
        'file_website': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'website.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        
        'file_comments': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'comments.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        
        'file_security': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'security.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'detailed',
            'encoding': 'utf-8',
        },
    },
    
    'loggers': {
        'django': {
            'handlers': ['console', 'file_all', 'file_errors'],
            'level': 'INFO',
            'propagate': False,
        },
        
        'website': {
            'handlers': ['console', 'file_website', 'file_errors'],
            'level': 'DEBUG',
            'propagate': False,
        },
        
        'website.comments': {
            'handlers': ['console', 'file_comments', 'file_errors'],
            'level': 'INFO',
            'propagate': False,
        },
        
        'security': {
            'handlers': ['console', 'file_security'],
            'level': 'WARNING',
            'propagate': False,
        },
        
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        
        'django.request': {
            'handlers': ['file_errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        
        'django.security': {
            'handlers': ['file_security'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
    
    'root': {
        'handlers': ['console', 'file_all'],
        'level': 'INFO',
    },
}

# ═══════════════════════════════════════════════════════════════════
# Ckeditor
# ═══════════════════════════════════════════════════════════════════

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moonocolor',
        'width': '100%',
        'height': '800px',
        'contentsCss': '/static/dashboard/css/editor.css',
        'extraAllowedContent': '*[*]{*}(*)',
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
            'cpp': 'C++',
            'bash': 'Bash',
            'xml': 'XML',
            'javascript': 'JavaScript',
            'json': 'JSON'
        },
        'stylesSet': [
            {
                'name': 'Код в тексте',
                'element': 'code',
            }
        ],
    }
}

# ═══════════════════════════════════════════════════════════════════
# Яндекс Метрика
# ═══════════════════════════════════════════════════════════════════

YANDEX_METRIKA_TOKEN = env('YANDEX_METRIKA_TOKEN')
YANDEX_METRIKA_COUNTER = env('YANDEX_METRIKA_COUNTER')

# ═══════════════════════════════════════════════════════════════════
# Dashboard
# ═══════════════════════════════════════════════════════════════════

DASHBOARD_CUSTOMIZATION = {
    'search_model': 'website.article',
    'sidebar_icons': {
        'auth.user': 'person',
        'auth.group': 'groups',
        'website.article': 'article',
        'website.category': 'category',
        'website.subcategory': 'bookmark',
        'website.comment': 'chat_bubble',
        'website.sitesettings': 'settings',
    },
    'hidden_apps': [
        'dashboard',
        'sites',
    ],
    'hidden_models': [
        'auth.group',
    ],
    'apps_order': [
        'website',
        'website.article',
        'website.comment',
        'website.category',
        'website.subcategory',
        'website.sitesettings',
        'auth',
    ],
    'extra_links': [
        {
            'website': [
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

# ═══════════════════════════════════════════════════════════════════
# Akismet
# ═══════════════════════════════════════════════════════════════════

IS_USE_AKISMET = env('IS_USE_AKISMET')
AKISMET_API_KEY = env('AKISMET_API_KEY')
AKISMET_URL = env('AKISMET_URL')
