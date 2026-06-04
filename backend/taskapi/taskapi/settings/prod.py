import os
from urllib.parse import parse_qs, urlparse

from .base import *

DEBUG = False

def database_config_from_url(database_url: str) -> dict:
    parsed_url = urlparse(database_url)
    query_params = parse_qs(parsed_url.query)

    sslmode = query_params.get('sslmode', [os.getenv('POSTGRES_SSLMODE', 'require')])[0]

    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parsed_url.path.lstrip('/'),
        'USER': parsed_url.username or '',
        'PASSWORD': parsed_url.password or '',
        'HOST': parsed_url.hostname or '',
        'PORT': parsed_url.port or 5432,
        'OPTIONS': {
            'sslmode': sslmode,
        },
        'CONN_MAX_AGE': 60,
    }


database_url = os.getenv('DATABASE_URL') or os.getenv('POSTGRES_CONNECTION_STRING')

if database_url:
    DATABASES = {
        'default': database_config_from_url(database_url),
    }
else:
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
