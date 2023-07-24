from django.core.management.utils import get_random_secret_key

pg_conn = {'username': 'postgres',
           'password': '736269',
           'host': 'localhost',
           'database': 'postgres',
           'port': 5432}

openweather_key = "25508d420f626cbc78680910ec16ccd5"
timezone_db_key = 'LGUOSL08JVU1'
django_key = get_random_secret_key()
