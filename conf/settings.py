"""
Django settings for ui project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

import environ

from directory_components.constants import IP_RETRIEVER_NAME_GOV_UK
from directory_constants.constants import cms
import directory_healthcheck.backends


env = environ.Env()
env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

# As the app is running behind a host-based router supplied by Heroku or other
# PaaS, we can open ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'raven.contrib.django.raven_compat',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'core',
    'contact',
    'opportunities',
    'directory_constants',
    'captcha',
    'directory_components',
    'crispy_forms',
    'directory_healthcheck',
]

MIDDLEWARE_CLASSES = [
    'directory_components.middleware.MaintenanceModeMiddleware',
    'directory_components.middleware.IPRestrictorMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'contact.middleware.GoogleCampaignMiddleware',
    'directory_components.middleware.NoCacheMiddlware',
    'directory_components.middleware.RobotsIndexControlHeaderMiddlware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'core.context_processors.untranslated_url',
                'core.context_processors.footer_contact_us_link',
                'directory_components.context_processors.analytics',
                'directory_components.context_processors.urls_processor',
                'directory_components.context_processors.cookie_notice',
                'directory_components.context_processors.feature_flags',
                (
                    'directory_components.context_processors.'
                    'header_footer_processor'
                ),
                (
                    'directory_components.context_processors.'
                    'invest_header_footer_processor'
                )
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'

VCAP_SERVICES = env.json('VCAP_SERVICES', {})

if 'redis' in VCAP_SERVICES:
    REDIS_URL = VCAP_SERVICES['redis'][0]['credentials']['uri']
else:
    REDIS_URL = env.str('REDIS_URL', '')

if REDIS_URL:
    cache = {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': "django_redis.client.DefaultClient",
        }
    }
else:
    cache = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }

CACHES = {
    'default': cache,
    'cms_fallback': cache,
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_L10N = True
USE_TZ = True


# https://github.com/django/django/blob/master/django/conf/locale/__init__.py
LANGUAGES = [
    ('en-gb', 'English'),               # English
    ('de', 'Deutsch'),                  # German
    ('ja', '日本語'),                    # Japanese
    ('zh-hans', '简体中文'),             # Simplified Chinese
    ('fr', 'Français'),                 # French
    ('es', 'español'),                  # Spanish
    ('pt', 'Português'),                # Portuguese
    ('ar', 'العربيّة'),                 # Arabic
    # ('ru', 'Русский'),                  # Russian
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

FEATURE_MAINTENANCE_MODE_ENABLED = env.bool(
    'FEATURE_MAINTENANCE_MODE_ENABLED', False
)

# needed only for dev local storage
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

# Static files served with Whitenoise and AWS Cloudfront
# http://whitenoise.evans.io/en/stable/django.html#instructions-for-amazon-cloudfront
# http://whitenoise.evans.io/en/stable/django.html#restricting-cloudfront-to-static-files
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_HOST = env.str('STATIC_HOST', '')
STATIC_URL = STATIC_HOST + '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Logging for development
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True,
            },
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }
else:
    # Sentry logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': (
                    'raven.contrib.django.raven_compat.handlers.SentryHandler'
                ),
                'tags': {'custom-tag': 'x'},
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }


ANALYTICS_ID = env.str('ANALYTICS_ID', '')

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', True)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', 16070400)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Sentry
RAVEN_CONFIG = {
    'dsn': env.str('SENTRY_DSN', ''),
    'processors': (
        'raven.processors.SanitizePasswordsProcessor',
        'core.sentry_processors.SanitizeEmailMessagesProcessor',
    )
}

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', True)

CSRF_COOKIE_SECURE = True

# Google Recaptcha
RECAPTCHA_PUBLIC_KEY = env.str('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env.str('RECAPTCHA_PRIVATE_KEY')
# NOCAPTCHA = True turns on version 2 of recaptcha
NOCAPTCHA = env.bool('NOCAPTCHA', True)

# Google tag manager
GOOGLE_TAG_MANAGER_ID = env.str('GOOGLE_TAG_MANAGER_ID', '')
GOOGLE_TAG_MANAGER_ENV = env.str('GOOGLE_TAG_MANAGER_ENV', '')
UTM_COOKIE_DOMAIN = env.str('UTM_COOKIE_DOMAIN')
PRIVACY_COOKIE_DOMAIN = env.str('PRIVACY_COOKIE_DOMAIN', '')

# django-storages for thumbnails
AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME', '')
AWS_DEFAULT_ACL = 'public-read'
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_ENCRYPTION = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_CUSTOM_DOMAIN = env.str('AWS_S3_CUSTOM_DOMAIN', '')
AWS_S3_URL_PROTOCOL = env.str('AWS_S3_URL_PROTOCOL', 'https:')

PREFIX_DEFAULT_LANGUAGE = False

LANGUAGE_COOKIE_NAME = 'django-language'

# directory CMS
DIRECTORY_CMS_API_CLIENT_BASE_URL = env.str('CMS_URL')
DIRECTORY_CMS_API_CLIENT_API_KEY = env.str('CMS_SIGNATURE_SECRET')
DIRECTORY_CMS_API_CLIENT_SENDER_ID = 'directory'
DIRECTORY_CMS_API_CLIENT_SERVICE_NAME = cms.INVEST
DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT = env.int(
    'DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT', 2
)

# directory clients
DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS = 60 * 60 * 24 * 30  # 30 days

# Contact email
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL')
IIGB_AGENT_EMAIL = env.str('IIGB_AGENT_EMAIL')
EMAIL_BACKED_CLASSES = {
    'default': 'django.core.mail.backends.smtp.EmailBackend',
    'console': 'django.core.mail.backends.console.EmailBackend'
}
EMAIL_BACKEND_CLASS_NAME = env.str('EMAIL_BACKEND_CLASS_NAME', 'default')
EMAIL_BACKEND = EMAIL_BACKED_CLASSES[EMAIL_BACKEND_CLASS_NAME]
EMAIL_HOST = env.str('EMAIL_HOST', '')
EMAIL_PORT = env.int('EMAIL_HOST_PORT', 587)
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = True

# LINKS TO OTHER SERVICES
DIRECTORY_CONSTANTS_URL_EXPORT_READINESS = env.str(
    'DIRECTORY_CONSTANTS_URL_EXPORT_READINESS', ''
)
DIRECTORY_CONSTANTS_URL_EXPORT_OPPORTUNITIES = env.str(
    'DIRECTORY_CONSTANTS_URL_EXPORT_OPPORTUNITIES', ''
)
DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS = env.str(
    'DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS', ''
)
DIRECTORY_CONSTANTS_URL_EVENTS = env.str(
    'DIRECTORY_CONSTANTS_URL_EVENTS', ''
)
DIRECTORY_CONSTANTS_URL_INVEST = env.str('DIRECTORY_CONSTANTS_URL_INVEST', '')
DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER = env.str(
    'DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER', ''
)
DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON = env.str(
    'DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON', ''
)
DIRECTORY_CONSTANTS_URL_FIND_A_BUYER = env.str(
    'DIRECTORY_CONSTANTS_URL_FIND_A_BUYER', ''
)

# feature flags
FEATURE_FLAGS = {
    'EXPORT_JOURNEY_ON': False,  # not used in this project
    'INTERNATIONAL_CONTACT_LINK_ON': env.bool(
        'FEATURE_INTERNATIONAL_CONTACT_LINK_ENABLED', False),
    # used by directory-components
    'SEARCH_ENGINE_INDEXING_OFF': env.bool(
        'FEATURE_SEARCH_ENGINE_INDEXING_DISABLED', False
    ),
    'EU_EXIT_BANNER_ON': env.bool(
        'FEATURE_EU_EXIT_BANNER_ENABLED', False
    ),
    # used by directory-components
    'MAINTENANCE_MODE_ON': env.bool('FEATURE_MAINTENANCE_MODE_ENABLED', False),
}

# Invest High Potential Opportunities
HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS = env.str(
    'HPO_GOV_NOTIFY_AGENT_EMAIL_ADDRESS',
)
HPO_GOV_NOTIFY_AGENT_TEMPLATE_ID = env.str(
    'HPO_GOV_NOTIFY_AGENT_TEMPLATE_ID', '064e2801-18f4-4342-a9e3-5eecddfa7d04'
)
HPO_GOV_NOTIFY_USER_TEMPLATE_ID = env.str(
    'HPO_GOV_NOTIFY_USER_TEMPLATE_ID',
    'a9285cb0-6acf-428f-94f7-2da7248d9ef0'
)
HPO_GOV_NOTIFY_USER_REPLY_TO_ID = env.str(
    'HPO_GOV_NOTIFY_USER_REPLY_TO_ID',
    '3deb5fc2-1032-4352-aa0a-c677548a9f02'
)

# directory forms api client
DIRECTORY_FORMS_API_BASE_URL = env.str('DIRECTORY_FORMS_API_BASE_URL')
DIRECTORY_FORMS_API_API_KEY = env.str('DIRECTORY_FORMS_API_API_KEY')
DIRECTORY_FORMS_API_SENDER_ID = env.str('DIRECTORY_FORMS_API_SENDER_ID')
DIRECTORY_FORMS_API_DEFAULT_TIMEOUT = env.int(
    'DIRECTORY_API_FORMS_DEFAULT_TIMEOUT', 5
)
DIRECTORY_FORMS_API_ZENDESK_SEVICE_NAME = env.str(
    'DIRECTORY_FORMS_API_ZENDESK_SEVICE_NAME', 'Invest in GB',
)

# Directory healthcheck
DIRECTORY_HEALTHCHECK_TOKEN = env.str('HEALTH_CHECK_TOKEN')
DIRECTORY_HEALTHCHECK_BACKENDS = [
    directory_healthcheck.backends.FormsAPIBackend,
]

# ip-restrictor
IP_RESTRICTOR_SKIP_CHECK_ENABLED = env.bool(
    'IP_RESTRICTOR_SKIP_CHECK_ENABLED', False
)
IP_RESTRICTOR_SKIP_CHECK_SENDER_ID = env.str(
    'IP_RESTRICTOR_SKIP_CHECK_SENDER_ID', ''
)
IP_RESTRICTOR_SKIP_CHECK_SECRET = env.str(
    'IP_RESTRICTOR_SKIP_CHECK_SECRET', ''
)
IP_RESTRICTOR_REMOTE_IP_ADDRESS_RETRIEVER = env.str(
    'IP_RESTRICTOR_REMOTE_IP_ADDRESS_RETRIEVER',
    IP_RETRIEVER_NAME_GOV_UK
)
RESTRICT_ADMIN = env.bool('IP_RESTRICTOR_RESTRICT_IPS', False)
ALLOWED_ADMIN_IPS = env.list('IP_RESTRICTOR_ALLOWED_ADMIN_IPS', default=[])
ALLOWED_ADMIN_IP_RANGES = env.list(
    'IP_RESTRICTOR_ALLOWED_ADMIN_IP_RANGES', default=[]
)
RESTRICTED_APP_NAMES = env.list(
    'IP_RESTRICTOR_RESTRICTED_APP_NAMES', default=['admin']
)
if env.bool('IP_RESTRICTOR_RESTRICT_UI', False):
    # restrict all pages that are not in apps API, healthcheck, admin, etc
    RESTRICTED_APP_NAMES.append('')
