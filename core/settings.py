"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from pathlib import Path
import os
from django.contrib.messages import constants
from environ import Env
import dj_database_url


env = Env()
Env.read_env()
ENVIRONMENT = env('ENVIRONMENT', default='development')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENVIRONMENT == 'development'

ALLOWED_HOSTS = ['eventease.up.railway.app', 'localhost', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://eventease.up.railway.app', 'http://eventease.up.railway.app']

SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
	"whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'django.contrib.sites',
    'django_cleanup.apps.CleanupConfig',
    'Platform.apps.PlatformConfig',
    'eventos',
    'account_manager',
    'admin_honeypot',
# apps django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'notifications',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
	"whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.urls'

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
                'Platform.context_processors.notifications_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# the postgres can come from your 'local' machine or from a host, like Railway or False if don't want to use it.
POSTGRES = env('POSTGRES_FROM')
if ENVIRONMENT == 'production' or POSTGRES == 'hosted':
    DATABASES['default'] = dj_database_url.parse(env('DATABASE_URL'))
if POSTGRES == 'local':
    DATABASES['default']["ENGINE"] = 'django.db.backends.postgresql'
    DATABASES['default']["NAME"] = env('DATABASE_NAME')
    DATABASES['default']["USER"] = env('DATABASE_USER')
    DATABASES['default']["PASSWORD"] = env('DATABASE_PASSWORD')
    DATABASES['default']["HOST"] = env('DATABASE_HOST')
    DATABASES['default']["PORT"] = env('DATABASE_PORT')

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# conf Authentication 

AUTHENTICATION_BACKENDS = [
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

]

SITE_ID = 1

AUTH_USER_MODEL = 'account_manager.User'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_MAX_EMAIL_ADDRESSES = 1
ACCOUNT_EMAIL_VERIFICATION = 'none'

ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'account_login'

ACCOUNT_FORMS = {
    'signup': 'account_manager.forms.CustomSignupForm',
    'login': 'account_manager.forms.CustomLoginForm',
    'change_password': 'account_manager.forms.CustomChangePasswordForm',
    'set_password': 'account_manager.forms.CustomSetPasswordForm',
    'reset_password': 'account_manager.forms.CustomResetPasswordForm',
    'reset_password_from_key': 'account_manager.forms.CustomResetPasswordKeyForm',

}

# ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 15
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_LOGIN_ON_GET = True

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DATETIME_INPUT_FORMATS = ["%d/%m/%Y %H:%M",]  # '25/10/2006 14:30'


DJANGO_NOTIFICATIONS_CONFIG = {
    'USE_JSONFIELD': True
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'templates/static'),
]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Media files
MEDIA_URL = '/media/'

if ENVIRONMENT == 'production' or POSTGRES == 'hosted':
    DEFAULT_FILE_STORAGE ='cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUD_NAME'),
    'API_KEY': env('CLOUD_API_KEY'),
    'API_SECRET': env('CLOUD_API_SECRET'),
    }
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    

# message
MESSAGE_TAGS = {
    constants.DEBUG: 'alert alert-primary',
    constants.ERROR: 'alert alert-danger',
    constants.WARNING: 'alert alert-warning',
    constants.SUCCESS: 'alert alert-success',
    constants.INFO: 'alert alert-info ',
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email config

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
