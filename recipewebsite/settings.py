import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv()


# ============ SECURITY SETTINGS ============

# SECRET_KEY from environment (generated on first setup)
SECRET_KEY = os.environ.get('SECRET_KEY')

# DEBUG mode from environment (defaults to False for safety)
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS from environment (defaults to localhost)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# ============ INSTALLED APPS ============

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

INSTALLED_APPS = [
    # Django admin and auth
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'compressor',
    'location_field.apps.DefaultConfig',
    'widget_tweaks',
    # Local app
    'recipewebsite'
]

# ============ COMPRESSION ============

COMPRESS_ENABLED = DEBUG  # Habilita compressão apenas em produção
COMPRESS_OFFLINE = False  # Desabilita compressão offline
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# ============ MIDDLEWARE ============

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============ URL & TEMPLATES ============

ROOT_URLCONF = 'recipewebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'recipewebsite.context_processor.categories_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'recipewebsite.wsgi.application'


# ============ DATABASE ============

# MySQL configuration from environment variables
# See https://docs.djangoproject.com/en/5.0/ref/settings/#databases
   
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

# ============ AUTHENTICATION ============

# Password validation rules
# See https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# ============ INTERNATIONALIZATION ============

# See https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# ============ STATIC & MEDIA FILES ============

# Static files configuration (CSS, JavaScript, Images)
# See https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
]

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files (user uploads)
MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

COMPRESS_ROOT = os.path.join(BASE_DIR, 'static')


# ============ DEFAULT SETTINGS ============

# Default primary key field type
# See https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'recipewebsite.User'

# ============ LOCATION FIELD CONFIGURATION ============

# OpenStreetMap configuration for geographic field
LOCATION_FIELD = {
    'map.provider': 'openstreetmap',
    'search.provider': 'nominatim',
    'map.zoom': 7,
    'map.center': [20, 0],
}
