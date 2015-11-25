from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd8kdgkppql4g7r',
        'USER': 'kgiwsnwewtgmxe',
        'PASSWORD': 'CQJgaeInizSYx42vTYCnzhW0zj',
        'HOST': 'ec2-54-83-53-120.compute-1.amazonaws.com',
        'PORT': '5432',

    }
}

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = [BASE_DIR.child('static')]