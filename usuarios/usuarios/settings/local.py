from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
        #'NAME': 'usersprobe',
        #'USER': 'raul',
        #'PASSWORD': '09973911',
        #'HOST': '172.16.90.108',
        #'PORT': '5432',

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
#STATICFILES_DIRS = [BASE_DIR.child('static')]
STATICFILES_DIRS = [BASE_DIR / 'static']

# Para archivos multimedia
MEDIA_URL = '/media/'
#MEDIA_ROOT = BASE_DIR.child('media')
MEDIA_ROOT = [BASE_DIR / 'media']
