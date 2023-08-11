# CITYFRAME
Group six's summer project for M.Sc. in Computer Science @UCD.

## Prerequisites:
- Python 3.9 or 3.10
- Postgres server up and running
- Node.js 18.16.1
- npm 9.8.0
- an OpenWeather API key for the developer tier or higher (https://openweathermap.org/full-price#current)
- a timezonedb API key (https://timezonedb.com/)

## How to run:

1. clone the repo
2. change to the `cityframe` directory (containing requirements.txt)
3. install the requirements by running `pip install -r requirements.txt`
4. in the`cityframe` directory, create a file `credentials.py` in which you add and complete the following with your credentials: <br>
`pg_conn = {'username': 'yourpostgresusername',
           'password': 'yourpostgrespassword',
           'host': 'yourpostgreshost' (e.g. localhost),
           'database': 'yourpostgresdatabase' (e.g. postgres),
           'port': yourpostgresport (e.g. 5432)}`<br><br>
`openweather_key = 'youropenweatherapikey'`<br><br>
`timezone_db_key = 'yourtimezonedbapikey'`<br><br>
`django_key = 'yourdjangokey'` (make one up yourself)<br><br>
5. change to the database directory at `cityframe/data/database`
6. run `dbsetup.py` using the appropriate command for your OS
   1. Mac/Windows: `python dbsetup.py` 
   2. Ubuntu: `python3 dbsetup.py`
7. change to the data_population_scripts directory at `cityframe/data/database/data_population_scripts`
8. run `populate_zones.py` using the appropriate command
   1. Mac/Windows: `python populate_zones.py` 
   2. Ubuntu: `python3 populate_zones.py`
9. change to the frontend directory at `cityframe/web_app/frontend`
10. run `npm install`
11. run `npm run build`
12. change to the web_app directory at `cityframe/web_app`
13. collect static files by running the appropriate command for your OS 
    1. Mac/Windows: `python manage.py collectstatic --clear --no-input` 
    2. Ubuntu: `python3 manage.py collectstatic --clear --no-input`
14. launch the Django server by running the appropriate command for your OS 
    1. Mac/Windows: `python manage.py runserver`
    2. Ubuntu: `python3 manage.py runserver`
15. visit `127.0.0.1:8000` (or, in case your Django server runs on a different host/port, go there)

