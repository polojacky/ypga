"""
Django settings for ypga project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'suipxuussul@n2$2$gabwep=0y@+59-$21@cg@z$(#_yqmc#5d'


# Application definition
INSTALLED_APPS = (
    'django_gearman_commands',
    'django_gearman',
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'smuggler',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pagination',
    'tools',
    'browse',
    'search',
    'news',
    'about',
    'download',
    'help',
    'blast',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    #"django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    #"django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'ypga.urls'

WSGI_APPLICATION = 'ypga.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "collectStatic")
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
PKL_DIR = os.path.join(MEDIA_ROOT, "pkl")
BLAST_DIR = os.path.join(MEDIA_ROOT, "blast")
GENOME_DIR = os.path.join(MEDIA_ROOT, "genome")
DOWNLOAD_DIR = os.path.join(MEDIA_ROOT, "download")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

PAGINATION_DEFAULT_PAGINATION = 10
PAGINATION_DEFAULT_WINDOW = 1
PAGINATION_INVALID_PAGE_RAISES_404 = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ypdb',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': '',
        'PORT': ''
    }
}

GRAPPELLI_ADMIN_TITLE = 'YODYP Admin'
GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

# #for celery
# import djcelery
# djcelery.setup_loader()
#
# BROKER_HOST = "localhost"
# BROKER_PORT = 5672
# BROKER_USER = "ypga"
# BROKER_PASSWORD = "ypga"
# BROKER_VHOST = "/"

#for gearman
GEARMAN_SERVERS = ['127.0.0.1']

SITE_ID = 1
#development server
if socket.gethostname() == 'jacky-PC':
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    TEMPLATE_DEBUG = True
    ALLOWED_HOSTS = ['127.0.0.1']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ypdb',
            'USER': 'root',
            'PASSWORD': 'mysql',
            'HOST': '',
            'PORT': ''
        }
    }
    #URL_PREFIX = '/ypga'

else:  #production server
    DEBUG = True
    TEMPLATE_DEBUG = True

    ADMINS = (
    ('Liu Yang', 'liuyang@bmi.ac.cn'),
    )
    ALLOWED_HOSTS = ['127.0.0.1','localhost','tody.bmi.ac.cn']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ypdb',
            'USER': 'ypga',
            'PASSWORD': 'system111',
            'HOST': '',
            'PORT': ''
        }
    }
    #URL_PREFIX = '/ypga'

