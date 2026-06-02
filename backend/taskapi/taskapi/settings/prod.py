import os

from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'postgres'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
        'HOST': os.getenv('POSTGRES_HOST', ''),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
        'OPTIONS': {
            'sslmode': os.getenv('POSTGRES_SSLMODE', 'require'),
        },
    }
}
