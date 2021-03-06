"""
Django settings for BenHoboCo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

GET_SOLO_TEMPLATE_TAG_NAME = 'get_solo'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b&r86v3qyzx=d^8p8k4$c!#imhb+jys*$g@yxz8#vt83@r-va_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# NOTE: Local server has to be in the first position!
ALLOWED_HOSTS = [
    '127.0.0.1:8000',
    'cs410.cs.ualberta.ca:41011',
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'crispy_forms',
    'solo',
    'core',
    'south',
    'images',
    'posts',
    'authors',
    'friends',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'BenHoboCo.urls'

WSGI_APPLICATION = 'BenHoboCo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'helix',
        'USER':'myuser',
        'PASSWORD':'mypass',
        'HOST':'leago.btrinh.com',
        'PORT':'3306',
    }
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_PATH = os.path.join( BASE_DIR, "static" )

STATICFILES_DIRS = (
    STATIC_PATH,
)


# Templates
TEMPLATE_PATH = os.path.join( BASE_DIR, "templates")

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join( BASE_DIR, 'media' )

LOGIN_URL = '/login/'
