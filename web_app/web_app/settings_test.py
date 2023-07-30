from .settings import *

# Disable the database creation during tests
DATABASES['default']['TEST'] = {
    'CREATE_DB': False,
    'MIRROR': 'default'
}
