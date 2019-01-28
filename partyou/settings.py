"""
Django settings for partyou project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from decouple import config, Csv
from functools import partial
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# auth
LOGIN_REDIRECT_URL = LOGOUT_REDIRECT_URL = 'base:home'

AUTH_USER_MODEL = 'base.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'collectfast',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'partyou.base',
    'partyou.catalog',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'partyou.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'partyou.catalog.context_processors.categories',
            ],
        },
    },
]

WSGI_APPLICATION = 'partyou.wsgi.application'

# Configuração Django Debug Toolbar

INTERNAL_IPS = config('INTERNAL_IPS', cast=Csv(), default='127.0.0.1')

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')  # pragma: no cover
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # pragma: no cover

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

default_db_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

parse_database = partial(dj_database_url.parse, conn_max_age=600)

DATABASES = {
    'default': config('DATABASE_URL', default=default_db_url, cast=parse_database)
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Recife'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# Configuração de ambiente de desenvolvimento (arquivos estáticos e mediafiles)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

COLLECTFAST_ENABLED = False

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')

# STORAGE CONFIGURATION IN S3 AWS
# ------------------------------------------------------------------------------

if AWS_ACCESS_KEY_ID:
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')  # pragma: no cover
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')  # pragma: no cover
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400', }  # pragma: no cover
    AWS_PRELOAD_METADATA = True  # pragma: no cover
    AWS_AUTO_CREATE_BUCKET = False  # pragma: no cover
    AWS_QUERYSTRING_AUTH = True  # pragma: no cover
    AWS_S3_CUSTOM_DOMAIN = None  # pragma: no cover

    COLLECTFAST_ENABLED = True  # pragma: no cover

    AWS_DEFAULT_ACL = 'private'  # pragma: no cover

    # Static Assets
    # ------------------------------------------------------------------------------
    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'  # pragma: no cover
    STATIC_S3_PATH = 'static'  # pragma: no cover
    STATIC_ROOT = f'/{STATIC_S3_PATH}/'  # pragma: no cover
    STATIC_URL = f'//s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/{STATIC_S3_PATH}/'  # pragma: no cover
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'  # pragma: no cover

    # Upload Media Folder
    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'  # pragma: no cover
    DEFAULT_S3_PATH = 'mediafiles'  # pragma: no cover
    MEDIA_ROOT = f'/{DEFAULT_S3_PATH}/'  # pragma: no cover
    MEDIA_URL = f'//s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/{DEFAULT_S3_PATH}/'  # pragma: no cover

    INSTALLED_APPS.append('s3_folder_storage')  # pragma: no cover
    INSTALLED_APPS.append('storages')  # pragma: no cover

# Configuração do Sentry, plataforma para monitoramento de erros.

SENTRY_DSN = config('SENTRY_DSN', default=None)

if SENTRY_DSN:

    sentry_sdk.init(  # pragma: no cover
        dsn=SENTRY_DSN, integrations=[DjangoIntegration()]
    )
