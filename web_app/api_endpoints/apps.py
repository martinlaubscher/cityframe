from django.apps import AppConfig
from psycopg_pool import ConnectionPool
from sqlalchemy import URL
from credentials import pg_conn


class ApiEndpointsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_endpoints'

    pool = None

    def ready(self):
        # runs upon start

        # db connection details
        pg_url = URL.create("postgresql", **pg_conn)

        # create connection pool
        ApiEndpointsConfig.pool = ConnectionPool(pg_url.render_as_string(hide_password=False), max_size=4)
