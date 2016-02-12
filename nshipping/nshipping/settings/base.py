from django.core.exceptions import ImproperlyConfigured
import json

from unipath import Path

BASE_DIR = Path(__file__).ancestor(3)

with open("secrets.json") as f:
    secrets = json.loads(f.read())

def get_secret(secret_name, secrets=secrets):
    try:
        return secrets[secret_name]
    except:
        msg = "la variable %s no existe" % secret_name
        raise ImproperlyConfigured(msg)

SECRET_KEY = get_secret('SECRET_KEY')


DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

LOCAL_APPS = (
    'apps.users',
    'apps.ingreso',
    'apps.profiles',
    'apps.manifiesto',
    'apps.salida',
)

THIRD_PARTY_APPS = (
    'rest_framework',
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'nshipping.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.child('templates')],
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

WSGI_APPLICATION = 'nshipping.wsgi.application'

LANGUAGE_CODE = 'es-pe'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'users.User'
