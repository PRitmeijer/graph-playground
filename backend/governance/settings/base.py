# settings/base.py

from pathlib import Path
import os
import sys
from datetime import timedelta
from typing import TYPE_CHECKING
from gqlauth.settings_type import GqlAuthSettings
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-ceo2h7*^!dmqj6+d$(pkita)zy!dcxwzgmgqbg2rl8t6_=q2oo')
DEBUG = os.getenv("DEBUG", default=False)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'strawberry_django',
    'gqlauth',
    'core.apps.CoreConfig',
    'user.apps.UserConfig',
    'authn.apps.AuthNConfig',
    'userstatus.apps.UserStatusConfig',
]

AUTH_USER_MODEL = 'user.User'

if TYPE_CHECKING:
    from gqlauth.jwt.types_ import TokenType
    from django.contrib.auth.base_user import AbstractBaseUser

def jwt_payload_handler(user: "AbstractBaseUser") -> "TokenType":
    # Import inside to avoid circular imports
    from apps.authn.encode import encode_jwt_dynamic
    return encode_jwt_dynamic(user)


GQL_AUTH = GqlAuthSettings(
    JWT_PAYLOAD_HANDLER=jwt_payload_handler,
    JWT_ALGORITHM='RS256',
    LOGIN_REQUIRE_CAPTCHA=False,
    REGISTER_REQUIRE_CAPTCHA=False,
    JWT_EXPIRATION_DELTA=timedelta(hours=48)
)

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
            ],
        },
    },
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = "urls"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'db_name'),
        'USER': os.getenv('POSTGRES_RUNTIME_USER', 'db_user'),
        'PASSWORD': os.getenv('POSTGRES_RUNTIME_PASSWORD', 'db_password'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

import logging
logging.info(os.getenv('POSTGRES_HOST'))

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'