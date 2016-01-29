from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd8amskmu4j5fet',
        'USER': 'xicedsyhbpwirk',
        'PASSWORD': 'VTUxbK5boYTqXChP1gtQRGCuSq',
        'HOST': 'ec2-54-204-39-67.compute-1.amazonaws.com',
        'PORT': '5432',

    }
}

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = [BASE_DIR.child('static')]
