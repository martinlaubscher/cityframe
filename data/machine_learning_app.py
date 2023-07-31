# This is a machine learning application intended to link the model derived from the data contained in the final compiled taxi/weather CSV file
# to the back end application. Data from the database will be provided on the next few days, and predictions will be returned based on the input.

# The model selected for the MVP is XGBoost, due to its significant performance increases over linear regression, random forest, and neural network implementation. For more details, see ml_test.ipynb

# Independent varaibles (input): day (1-31), month (1-12), hour (0-23), week (see mapping key), temp (kelvin), feels_like (kelvin), weather_main (see mapping key), taxi_zone (see taxi zone list)
# Dependent varaible (output): Activity(float)

# Taxi Zone List: [4, 24, 12, 13, 41, 45, 42, 43, 48, 50, 68, 79, 74, 75, 87, 88, 90, 125, 100, 103, 107, 113, 114, 116, 120, 127, 128, 151, 140, 137, 141, 142, 152, 143, 144, 148, 153, 158, 161, 162, 163, 164, 170, 166, 186, 194, 202, 209, 211, 224, 229, 230, 231, 239, 232, 233, 234, 236, 237, 238, 263, 243, 244, 246, 249, 261, 262]

# Weather Mapping: {'Clear':1, 'Clouds':2, 'Drizzle': 3, 'Fog':4, 'Haze': 5, 'Mist':6, 'Rain': 7, 'Smoke': 8, 'Snow': 9, 'Squall': 10, 'Thunderstorm': 11}

# Week Mapping: {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6 }

import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
cityframe_path = os.path.dirname(current_path)
csv_path = os.path.join(current_path, "ml_ready_df.csv")
pkl_path = os.path.join(current_path, "model.pkl")

sys.path.append(cityframe_path)

import pickle
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sqlalchemy import create_engine, URL
from credentials import pg_conn


# machine learning app object
class MachineLearning:

    # initializes MachineLearning object with parameters for the data and pickle filepaths
    def __init__(self, dataFilePath=csv_path, pickleFilePath=pkl_path):
        """
        Args: pickleFilePath: string(must be valid filepath), dataFilePath: string(must be valid filepath)
        """

        self.dataFilePath = dataFilePath
        self.pickleFilePath = pickleFilePath
        self.engine = create_engine(URL.create("postgresql+psycopg", **pg_conn))

    def calculate_metrics(self, y_true, y_pred):
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        return rmse, mape

    # Trains the machine learning model and saves it as a pickle file
    def model_train(self, n=10000, params={"objective": "reg:tweedie", "tree_method": "hist"}):

        """
        Args: n (int), params (dictionary of xgboost parameters)
        Returns: pickled machine learning model (pickle file)
        """

        # data for model
        df = pd.read_csv(self.dataFilePath, keep_default_na=True, delimiter=',', skipinitialspace=True)

        # Training model on full data, as performance has already been evaluated
        xgb_x_train = df[['day', 'month', 'week', 'hour', 'temp', 'feels_like', 'weather_main', 'taxi_zone']]
        xgb_y_train = df['activity']

        # Genrating the model
        # creating xgboost regression models
        dtrain_reg = xgb.DMatrix(xgb_x_train, xgb_y_train, enable_categorical=True)

        print('training')

        # training model based on paramaters defined in function call
        model = xgb.train(
            params=params,
            dtrain=dtrain_reg,
            num_boost_round=n,
        )

        # Pickling the model
        with open(self.pickleFilePath, "wb") as f:
            pickle.dump(model, f)

        # Calculate metrics on the training data
        train_predictions = model.predict(dtrain_reg)
        rmse, mape = self.calculate_metrics(xgb_y_train, train_predictions)
        print("Training Root Mean Squared Error (RMSE):", rmse)
        print("Training Mean Absolute Percentage Error (MAPE):", mape)

        with open(self.pickleFilePath, "rb") as f:
            pkl = pickle.load(f)

        return pkl

    # Loads the pickle file. If it does not yet exist, the pickle model will be generated using the model_train() function
    def pickle_load(self):

        """
        Args: N/A
        Returns: pickled machine learning model (pickle file)
        """

        # checking for pickle of model
        if os.path.isfile(self.pickleFilePath):

            with open(self.pickleFilePath, "rb") as f:
                pkl = pickle.load(f)

        else:
            pkl = self.model_train()

        return pkl

    # fetches the data from the postgreSQL
    def fetch_data(self):

        """
        Args: N/A
        Returns: pandas dataframe
        """

        df = pd.DataFrame()

        try:
            with self.engine.begin() as connection:

                sql = "SELECT dt, (dt_iso AT TIME ZONE 'America/New_York') as dt_iso, temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, wind_speed, wind_deg, wind_gust, pop, rain_1h, snow_1h, clouds_all, weather_id, weather_main, weather_description, weather_icon FROM cityframe.weather_fc"

                df = pd.read_sql_query(sql, connection)

        except Exception as ex:
            print(ex)

        return df

    # Helper function to map weather codes to descriptions based on ranges
    def map_weather_description(self, code):

        """
        Args: code (int)
        Returns: Description (int)
        """

        weather_ranges = {(200, 299, 11), (300, 399, 3), (500, 599, 7), (600, 699, 9), (801, 900, 2), (701, 701, 6),
                          (711, 711, 8), (771, 771, 10), (800, 800, 1), (741, 741, 4), (721, 721, 5)}
        for start, end, description in weather_ranges:
            if start <= code <= end:
                return description
        return 0

    # formats the dataframe from the  database for processing by the machine learning model
    def data_prep(self):

        """
        Args: N/A
        Returns: Pandas dataframe
        """

        df = self.fetch_data()

        ml_ready_df = pd.DataFrame(columns=['taxi_zone'])
        ml_ready_df['taxi_zone'] = [4, 24, 12, 13, 41, 45, 42, 43, 48, 50, 68, 79, 74, 75, 87, 88, 90, 125, 100, 103,
                                    107, 113, 114, 116, 120, 127, 128, 151, 140, 137, 141, 142, 152, 143, 144, 148, 153,
                                    158, 161, 162, 163, 164, 170, 166, 186, 194, 202, 209, 211, 224, 229, 230, 231, 239,
                                    232, 233, 234, 236, 237, 238, 263, 243, 244, 246, 249, 261, 262]

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
        Args: pandas dataframe
        """

        df.to_sql('Results', self.engine, schema='cityframe', if_exists='replace', index=False)

        return None

    # main function to be called by back-end
    def machine_learn(self):

        """
        Args: N/A
        Returns: Pandas Dataframe
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

        df = df[['taxi_zone', 'prediction', 'bucket']]
        df['dt_iso'] = dt_iso.dt.tz_localize('America/New_York')

        df['id'] = range(1, len(df) + 1)

        self.create_db(df)

        return None


def main():
    c = MachineLearning()

    c.machine_learn()


if __name__ == '__main__':
    main()
