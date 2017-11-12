import os

from .utils import (
    load_permissions, load_groups, load_managed_user_permissions, load_managed_user_groups
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Force a subpath for DJANGO, useful for mounting behind a proxy
FORCE_SCRIPT_NAME = os.environ.get('FORCE_SCRIPT_NAME', '/')

SECRET_KEY = os.environ['SECRET_KEY']
ENVIRONMENT = os.environ['ENVIRONMENT'].lower()
USE_SSL = os.environ.get('USE_SSL', False)

DEBUG = ENVIRONMENT == 'dev'

if ENVIRONMENT == 'dev':
    ENVIRONMENT_COLOR = 'gray'
elif ENVIRONMENT == 'test':
    ENVIRONMENT_COLOR = 'orange'
else:
    ENVIRONMENT_COLOR = 'red'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd-party apps.
    'oauth2_provider',
    'rest_framework',

    # Project apps.
    'managed_users',
    'oauth',
    'users',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
    ),
}

if not DEBUG:
    # Don't include the browsable API renderer outside of Development.
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
    )

if DEBUG:
    # For convenience, we can access the API Browser in Development.
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += [
        'rest_framework.authentication.SessionAuthentication',
    ]

AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend'
)

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Global read access',
        'write': 'Global write access',
    }
}
OAUTH_REDIRECT_PARAM = 'next'

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'oauth_microservice.urls'

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
                'oauth_microservice.context_processors.from_settings',
            ],
        },
    },
]

# Allow for external services (Docker, etc) to supply override template.
# Note: It must be inserted first to override the existing templates.
EXTERNAL_TEMPLATES = os.environ.get('EXTERNAL_TEMPLATES', None)
if EXTERNAL_TEMPLATES:
    TEMPLATES[0]['DIRS'].insert(0, EXTERNAL_TEMPLATES)


WSGI_APPLICATION = 'oauth_microservice.wsgi.application'

SITENAME = 'OAuth Microservice'


# Security

SECURE_HSTS_SECONDS = 518400
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_HTTPONLY = True

if USE_SSL:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True

if not DEBUG and USE_SSL:
    # See notes at https://docs.djangoproject.com/en/1.10/ref/settings/
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DB_USERNAME'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
    }
}


# Password validation

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


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'staticfiles'))

# Registration

ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window
REGISTRATION_OPEN = False
LOGIN_URL = '/permissions/'

# Permissions Settings

PERMISSIONS_PATH = os.environ.get('PERMISSIONS_PATH', os.path.join(BASE_DIR, 'permissions.yaml'))
DEFAULT_PERMISSIONS = load_permissions(PERMISSIONS_PATH)
DEFAULT_GROUPS = load_groups(PERMISSIONS_PATH)

# Managed Users Settings

ENABLE_REMOTE_USER_MANAGEMENT = bool(os.environ.get('ENABLE_REMOTE_USER_MANAGEMENT', False))
if ENABLE_REMOTE_USER_MANAGEMENT:
    REMOTE_USER_MANAGEMENT = {
        # The Permission that a user must have in order to create new managed users.
        'MANAGING_USER_PERMISSION': os.environ['MANAGING_USER_PERMISSION'],
        # A list of permissions to give newly created managed users.
        'MANAGED_USERS': {
            'DEFAULT_GROUPS': load_managed_user_groups(PERMISSIONS_PATH),
            'DEFAULT_PERMISSIONS': load_managed_user_permissions(PERMISSIONS_PATH),
        }
    }
else:
    REMOTE_USER_MANAGEMENT = None


# Email Settings

EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_TIMEOUT = 10
EMAIL_USE_TLS = True if ENVIRONMENT.startswith('prod') else False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
