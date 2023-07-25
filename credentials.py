from django.core.management.utils import get_random_secret_key

pg_conn = {'username': 'postgres',
           'password': '736269',
           'host': 'localhost',
           'database': 'postgres',
           'port': 5432}

openweather_key = "2a2c58218303f9b901149f60e812f72c"
timezone_db_key = 'LGUOSL08JVU1'
django_key = get_random_secret_key()
