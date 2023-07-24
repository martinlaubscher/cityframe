# This is a machine learning application intended to link the model derived from the data contained in the final compiled taxi/weather CSV file
# to the back end application. Data from the database will be provided on the next few days, and predictions will be returned based on the input.

# The model selected for the MVP is XGBoost, due to its significant performance increases over linear regression, random forest, and neural network implementation. For more details, see ml_test.ipynb

# Independent varaibles (input): day (1-31), month (1-12), hour (0-23), week (see mapping key), temp (kelvin), feels_like (kelvin), weather_main (see mapping key), taxi_zone (see taxi zone list)
# Dependent varaible (output): Activity(float)

# Taxi Zone List: [7,  88,  90, 125, 100, 103, 107, 113, 114, 116, 120, 127, 128, 151, 140, 137, 141, 142, 152, 143, 144, 148, 153, 158, 161, 162, 163, 164, 170, 166, 186, 194, 202, 209, 211, 224, 229, 230, 231, 239, 232, 233, 234, 236, 237, 238, 263, 243, 244, 246, 249, 261, 262]

# Weather Mapping: {'Clear':1, 'Clouds':2, 'Drizzle': 3, 'Fog':4, 'Haze': 5, 'Mist':6, 'Rain': 7, 'Smoke': 8, 'Snow': 9, 'Squall': 10, 'Thunderstorm': 11}

# Week Mapping: {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6 }


import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(current_path)
print(cityframe_path)

sys.path.append(cityframe_path)

import pickle
import xgboost as xgb
import pandas as pd
import psycopg
from sqlalchemy import create_engine
from sqlalchemy import inspect, create_engine, Table, URL, MetaData, Column, Integer, BigInteger, String, Float, \
    DateTime
from sqlalchemy.schema import CreateSchema
from io import StringIO
from credentials import pg_conn


# machine learning app object
class MachineLearning:

    def __init__(self, dataFilePath='./ml_ready_df.csv', pickleFilePath='./model.pkl'):
        """
        initializes filepaths for source data and pickle file

        Input: pickleFilePath: string(must be valid filepath), dataFilePath: string(must be valid filepath)
        """

        self.dataFilePath = dataFilePath
        self.pickleFilePath = pickleFilePath

    # Loads the pickle file. If it does not yet exist, the pickle model will be generated
    def pickle_load(self):

        """
        Input: none
        Output: pickle object 

        #INSERT THE PROPER FILEPATHS WHEN SETTING UP
        #MAKE SURE THE PICKLE FILE SAVES TO THE SAME FOLDER AS THIS FILE
        """

        # checking for pickle of model
        if os.path.isfile(self.pickleFilePath):

            with open(self.pickleFilePath, "rb") as f:
                pkl = pickle.load(f)

        else:

            # data for model
            df = pd.read_csv(self.dataFilePath, keep_default_na=True, delimiter=',', skipinitialspace=True)

            # Training model on full data, as performance has already been evaluated
            xgb_x_train = df[['day', 'month', 'week', 'hour', 'temp', 'feels_like', 'weather_main', 'taxi_zone']]
            xgb_y_train = df['activity']

            # Genrating the model
            # creating xgboost regression models
            dtrain_reg = xgb.DMatrix(xgb_x_train, xgb_y_train, enable_categorical=True)

            # defining parameters and training
            params = {"objective": "reg:squarederror", "tree_method": "hist"}
            n = 10000

            model = xgb.train(
                params=params,
                dtrain=dtrain_reg,
                num_boost_round=n,
            )

            # Pickling the model
            with open(self.pickleFilePath, "wb") as f:
                pickle.dump(model, f)

            with open(self.pickleFilePath, "rb") as f:
                pkl = pickle.load(f)

        # closing pickle file
        f.close()

        return pkl

    # fetches the data from the postgreSQL
    def fetch_data(self):

        """
        input: none
        output: pandas dataframe
        """

        # df = pd.DataFrame
        df = pd.DataFrame()

        pg_url = URL.create(
            "postgresql",
            **pg_conn
        )

        try:
            conn = psycopg.connect(pg_url.render_as_string(hide_password=False))
            cur = conn.cursor()

            sql = "SELECT dt, (dt_iso AT TIME ZONE 'America/New_York') as dt_iso, temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, wind_speed, wind_deg, wind_gust, pop, rain_1h, snow_1h, clouds_all, weather_id, weather_main, weather_description, weather_icon FROM cityframe.weather_fc"
            df = pd.read_sql_query(sql, conn)

        except Exception as ex:
            print(ex)

        cur.close()
        conn.close()

        return df

    # Helper function to map weather codes to descriptions based on ranges
    def map_weather_description(self, code):
        weather_ranges = {(200, 299, 11), (300, 399, 3), (500, 599, 7), (600, 699, 9), (801, 900, 2), (701, 701, 6),
                          (711, 711, 8), (771, 771, 10), (800, 800, 1), (741, 741, 4), (721, 721, 5)}
        for start, end, description in weather_ranges:
            if start <= code <= end:
                return description
        return 0

    # formats the dataframe from the  database for processing by the machine learning model
    def data_prep(self):

        """
        Args: none
        Output: Pandas dataframe
        """

        df = self.fetch_data()

        ml_ready_df = pd.DataFrame(columns=['taxi_zone'])
        # ml_ready_df['taxi_zone'] = [7, 88, 90, 125, 100, 103, 107, 113, 114, 116, 120, 127, 128, 151, 140, 137, 141,
        #                             142, 152, 143, 144, 148, 153, 158, 161, 162, 163, 164, 170, 166, 186, 194, 202, 209,
        #                             211, 224, 229, 230, 231, 239, 232, 233, 234, 236, 237, 238, 263, 243, 244, 246, 249,
        #                             261, 262]
        ml_ready_df['taxi_zone'] = [4, 12, 13, 24, 41, 42, 43, 45, 48, 50, 68, 74, 75, 79, 87, 88, 90, 100, 103, 107,
                                    113, 114, 116, 120, 125, 127, 128, 137, 140, 141, 142, 143, 144, 148, 151, 152, 153,
                                    158, 161, 162, 163, 164, 166, 170, 186, 194, 202, 209, 211, 224, 229, 230, 231, 232,
                                    233, 234, 236, 237, 238, 239, 243, 244, 246, 249, 261, 262, 263]

        df['dt_iso'] = df['dt_iso']
        df['month'] = df['dt_iso'].dt.month
        df['day'] = df['dt_iso'].dt.day
        df['hour'] = df['dt_iso'].dt.hour
        week_map = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6}
        df['week'] = df['dt_iso'].dt.day_name().map(week_map)
        df['weather_main'] = df['weather_id'].apply(self.map_weather_description)
        df['weather_main'] = df['weather_main'].fillna(0)

        n_zones = len(ml_ready_df['taxi_zone'].unique())
        dt_iso = pd.Series(df['dt_iso'].tolist() * n_zones)

        df = df[['day', 'month', 'week', 'hour', 'temp', 'feels_like', 'weather_main']]

        ml_ready_df = ml_ready_df.assign(key=1).merge(df.assign(key=1), on='key').drop('key', axis=1)
        ml_ready_df = ml_ready_df[['day', 'month', 'week', 'hour', 'temp', 'feels_like', 'weather_main', 'taxi_zone']]

        return ml_ready_df, dt_iso

    # creates a new database to hold results
    def create_db(self, df):

        """
        input: pandas dataframe
        output: none
        """

        pg_url = URL.create(
            "postgresql",
            **pg_conn
        )

        engine = create_engine(pg_url)

        df.to_sql('Results', engine, schema='cityframe', if_exists='replace', index=False)

        return None

    # main function to be called by back-end
    def machine_learn(self):

        """
        Input: none
        Output: Pandas Dataframe
        """

        df, dt_iso = self.data_prep()

        pkl = self.pickle_load()

        # predicting data fpr each row
        prediction_data = xgb.DMatrix(df, enable_categorical=True)
        predictions = pkl.predict(prediction_data)

        df['prediction'] = predictions

        # bucketing predictions
        df['bucket'] = pd.qcut(df['prediction'], q=5, labels=range(1, 6))
        df['bucket'] = df['bucket'].astype(int)

        df = df[['month', 'day', 'hour', 'taxi_zone', 'prediction', 'bucket']]
        df['dt_iso'] = dt_iso.dt.tz_localize('America/New_York')

        df['id'] = range(1, len(df) + 1)

        self.create_db(df)

        return None


c = MachineLearning()

c.machine_learn()
