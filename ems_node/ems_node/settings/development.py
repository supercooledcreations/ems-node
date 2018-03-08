import os
from .base import BASE_DIR

DEBUG = True

SECRET_KEY = 'fakekey123fakekey123fakekey123fakekey123fakekey123fakekey123'

ALLOWED_HOSTS = []

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}