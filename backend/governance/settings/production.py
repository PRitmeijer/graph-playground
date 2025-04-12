# settings/production.py

from .base import *

DEBUG = False

# Use environment variables or specific DB configurations for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'db'),
        'USER': os.getenv('POSTGRES_RUNTIME_USER', 'db_user'),
        'PASSWORD': os.getenv('POSTGRES_RUNTIME_PASSWORD', 'db_password'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# Let superuser of db run migrations & loaddata this way, RLS can be bypassed and enforced on the runtimeuser.
if 'makemigrations' in sys.argv or 'migrate' in sys.argv or 'loaddata' in sys.argv:
    DATABASES['default']['USER'] = os.getenv('POSTGRES_USER', 'django_migrate')
    DATABASES['default']['PASSWORD'] = os.getenv('POSTGRES_PASSWORD', 'migrate_password')

# Additional production settings like security and optimizations
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
         'console': {
              'class': 'logging.StreamHandler',
         },
    },
    'loggers': {
         # This configures the root logger; you can also set up your module specifically.
         '': {
              'handlers': ['console'],
              'level': 'DEBUG',
         },
    },
}