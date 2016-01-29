from .base import *
# erroes en modo local
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('USER'),
        'PASSWORD': get_secret('PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',

    }
}

STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR.child('static')]
