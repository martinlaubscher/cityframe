from .settings import *
from credentials import pg_test_conn

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': pg_test_conn['database'],
        'USER': pg_test_conn['username'],
        'PASSWORD': pg_test_conn['password'],
        'HOST': pg_test_conn['host'],
        'PORT': pg_test_conn['port'],
        'OPTIONS': {
            'options': '-c search_path=test_schema'
        }
    }
}

TEST_RUNNER = 'web_app.test_runner.TestRunner'