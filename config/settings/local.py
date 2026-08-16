from .base import *

import os
from dotenv import load_dotenv

load_dotenv()

# Local muhit uchun maxfiy kalit va debug
SECRET_KEY = os.getenv('SECRET', 'django-insecure-default-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# Local SQLite ma'lumotlar bazasi
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Konsolga xat yuborish (Email soxat rejimida)
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}