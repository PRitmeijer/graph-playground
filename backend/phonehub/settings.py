# settings.py
import os
from settings.base import *  # Import common settings from base.py

# Load environment-specific settings
if os.getenv('DJANGO_ENV') == 'production':
    from settings.production import *
else:
    from settings.local import *
