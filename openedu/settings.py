"""
Django settings for openedu project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import os
import sys
import djcelery

djcelery.setup_loader()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
DEBUG = True

ALLOWED_HOSTS = ["212.193.82.110", "openedu.urfu.ru", "*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'phonenumber_field',
    'auth_backends',
    'graphene_django',
    'corsheaders',
    'export_action',
    'smuggler',
    'minors',
    'home',
    'other',
    'roo',
    'reversion',
    'openprofession',
    'questionnaire',
    'ellada_api',
    'django_celery_results',
    'advanced_filters',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'auth_backends.backends.EdXOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'courses.openprofession.ru',
    'studio.openprofession.ru',
    'https://courses.openedu.urfu.ru/',

)
ROOT_URLCONF = 'openedu.urls'

TEMPLATES_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.request',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.static',
    'django.template.context_processors.media',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
    {
        'BACKEND': 'openedu.mako_templates.MakoTemplates',
        'APP_DIRS': False,
        'DIRS': [os.path.join(BASE_DIR, 'mako_templates')],
        'OPTIONS': {
            # 'module_directory': '/home/me/mako_output',
            'context_processors': TEMPLATES_CONTEXT_PROCESSORS,
            'strict_undefined': True
        }
    }
]

WSGI_APPLICATION = 'openedu.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/usr/local/itoo/var/log/openedu/app.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'celery_task_logger': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'filename': '/tmp/celery_tasks.log',
        },
        # 'celery_task_logger': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': '/tmp/celery_tasks.log',
        #     'maxBytes': 1024 * 1024 * 5,
        #     'backupCount': 2,
        #     'formatter': 'standard'
        # },
    },
    'loggers': {
        'INFO': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cacheback': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'celery_logging': {
            'handlers': ['celery_task_logger'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/files/openedu_static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
MEDIA_URL = '/uploads/'

LMS = "http://courses.openedu.urfu.ru/"
LMS_API_COURSES = "api/courses/v1/courses/"

DEFAULT_FROM_EMAIL = "openedu@urfu.ru"

SOCIAL_AUTH_EDX_OAUTH2_ENDPOINT = "https://courses.openedu.urfu.ru/oauth2"

SOCIAL_AUTH_STRATEGY = 'auth_backends.strategies.EdxDjangoStrategy'

# LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'https://openedu.urfu.ru/'

GRAPHENE = {
    'SCHEMA': 'openprofession.schema.schema',
    'MIDDLEWARE': (
        'graphene_django.debug.DjangoDebugMiddleware',
    )
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 200000  # тут поменьше сделать
LOGIN_URL = '/admin/login'



