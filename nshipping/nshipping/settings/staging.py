from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']
#configuracion de bd
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd4e4qqitffoqpc',
        'USER': 'dfbzblewnwmixv',
        'PASSWORD': 'Ht07CgFYbixXBHns8ALyC_3NrA',
        'HOST': 'ec2-107-20-136-89.compute-1.amazonaws.com',
        'PORT': '5432',

    }
}

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = [BASE_DIR.child('static')]
