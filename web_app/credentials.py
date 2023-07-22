from django.core.management.utils import get_random_secret_key

pg_conn = {'username': 'jingao',
           'password': 'jingaoDjango',
           'host': 'localhost',
           'database': 'cityframe',
           'port': 5432}

openweather_key = "25508d420f626cbc78680910ec16ccd5"
timezone_db_key = 'LGUOSL08JVU1'
django_key = get_random_secret_key()

# db_name = 'cityframe'
# db_user = 'jingao'
# db_password = 'jingaoDjango'
# db_host = 'localhost'
# db_port = '5432'
# django_key = get_random_secret_key()