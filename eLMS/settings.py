"""
Django settings for eLMS project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os

from pathlib import Path

import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN").strip(),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY").strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['presenttruth.herokuapp.com','127.0.0.1','www.presenttruthers.com','presenttruthers.com','34.42.99.68','34.16.171.81',
                 "34.125.149.128","0.0.0.0","adventproclaimer.com","34.16.208.222",
                 "e8fd-197-180-95-83.ngrok-free.app","dc22-2c0f-2a80-10d0-8d10-b55d-a7e-d40e-2e5a.ngrok-free.app",
                 "8000-lunyamwidev-adventprocl-cm1tuigzf0n.ws-eu114.gitpod.io","89.117.60.173"]

CSRF_TRUSTED_ORIGINS = ["https://adventproclaimer.com","https://presenttruth.herokuapp.com",'http://34.42.99.68',
                        "http://34.16.208.222/",
                        "https://34.16.208.222",
                        "http://adventproclaimer.com/",
                        "https://adventproclaimer.com/",
                        "https://e8fd-197-180-95-83.ngrok-free.app",
                        "https://dc22-2c0f-2a80-10d0-8d10-b55d-a7e-d40e-2e5a.ngrok-free.app",
                        "https://8000-lunyamwidev-adventprocl-cm1tuigzf0n.ws-eu114.gitpod.io","http://89.117.60.173/","https://89.117.60.173/"]

# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig',
    'discussion.apps.DiscussionConfig',
    'attendance.apps.AttendanceConfig',
    'quiz.apps.QuizConfig',
    'django_cleanup.apps.CleanupConfig',
    'froala_editor',
    'django_celery_beat',
    'django_celery_results',
    'messenger',
    'health',
    'crispy_forms',
    "crispy_bootstrap5",
    'payment',
    'paypal.standard.ipn',
    'helpers',
    'rest_framework',
    'needs',
    'appointment',
    'memberships',
    'evangelism',
    'store',
    'stripe',
    'widget_tweaks',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'tinymce',
    'marketing',
    'posts',
    'chunked_upload',
    'typist',
    'musick',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",

]

ROOT_URLCONF = 'eLMS.urls'
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
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


WSGI_APPLICATION = 'eLMS.wsgi.application'

ASGI_APPLICATION = "eLMS.asgi.application"
# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'elms',
#         'HOST': 'localhost',
#         'USER': 'root',
#         'PASSWORD': '',
#     }
# }

# settings.py

# settings.py

AUTH_USER_MODEL = 'auth.User'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / "db.sqlite3",  # Assuming db.sqlite3 is in the project's base directory
#     }
# }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DBNAME").strip(),
        "USER": os.getenv("POSTGRES_USER").strip(),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD").strip(),
        "HOST": os.getenv("POSTGRES_HOST").strip(),
        "PORT": os.getenv("POSTGRES_PORT").strip(),
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    # 'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    # 'django.contrib.auth.hashers.UnsaltedSHA1PasswordHasher',
    # 'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
    # 'django.contrib.auth.hashers.CryptPasswordHasher',
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# STATIC_URL = 'static/'
# STATIC_ROOT = 'static/'
STATIC_URL = '/static/'


STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = '/usr/src/app/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TINYMCE_DEFAULT_CONFIG = {
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY').strip()
MAILCHIMP_DATA_CENTER = os.getenv('MAILCHIMP_DATA_CENTER').strip()
MAILCHIMP_EMAIL_LIST_ID = os.getenv('MAILCHIMP_EMAIL_LIST_ID').strip()
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER').strip()


STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY').strip()
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY').strip()

# EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER').strip()
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD').strip()
EMAIL_PORT = 587
EMAIL_USE_TLS = True


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

PAYPAL_RECEIVER_EMAIL = "lunyamwi777@gmail.com"
PAYPAL_BUY_BUTTON_IMAGE = "https://res.cloudinary.com/djqomicoa/image/upload/v1714855978/donation_button_jvxjjv.jpg"
PAYPAL_TEST = True  # Set to False for production
PAYPAL_CLIENT_ID = 'your_paypal_client_id'
PAYPAL_CLIENT_SECRET = 'your_paypal_client_secret'
PAYPAL_MODE = 'sandbox'  # or 'live' for production


MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
MPESA_CONSUMER_SECRET= os.getenv("MPESA_CONSUMER_SECRET")
MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")
MPESA_SHORT_CODE = os.getenv("MPESA_SHORT_CODE")
MPESA_CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL")
MPESA_API_URL=os.getenv("MPESA_API_URL")
MPESA_AUTH_URL= os.getenv("MPESA_AUTH_URL")
MPESA_STKPUSH=os.getenv("MPESA_STKPUSH")

# settings.py

# Set the maximum size of the request body to 10MB (10 * 1024 * 1024 bytes)
FILE_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024