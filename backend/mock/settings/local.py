# settings/local.py

from .base import *

DEBUG = True

# Override database settings for local environment (use SQLite for local dev)
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}

# Optional: Add other local development settings
