from django.core.management.utils import get_random_secret_key

pg_conn = {'username': 'postgres',
           'password': '736269',
           'host': 'localhost',
           'database': 'postgres',
           'port': 5432}

openweather_key = "dadd1bf4240392ee40c8a8c4bc81ce0b"
timezone_db_key = 'LGUOSL08JVU1'
django_key = get_random_secret_key()
