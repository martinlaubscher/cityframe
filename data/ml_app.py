#This is a machine learning application intended to link the model derived from the data contained in the final compiled taxi/weather CSV file
#to the back end application. Data from the database will be provided on the next few days, and predictions will be returned based on the input.

#The model selected for the MVP is XGBoost, due to its significant performance increases over linear regression, random forest, and neural network implementation. For more details, see ml_test.ipynb

#Independent varaibles (input): day (1-31), month (1-12), hour (0-23), week (see mapping key), temp (kelvin), feels_like (kelvin), weather_main (see mapping key), taxi_zone (see taxi zone list)
#Dependent varaible (output): Activity(float)

#Taxi Zone List: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265]

#Weather Mapping: {'Clear':1, 'Clouds':2, 'Drizzle': 3, 'Fog':4, 'Haze': 5, 'Mist':6, 'Rain': 7, 'Smoke': 8, 'Snow': 9, 'Squall': 10, 'Thunderstorm': 11}

#Week Mapping: {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6 }

import os
import pickle
import xgboost as xgb
import pandas as pd

#Loads the pickle file. If it does not yet exist, the pickle model will be generated
def pickle_load(dataFilePath = 'C:/Users/mattx/Downloads/data/data/cleaned data/ml_ready_df.csv', pickleFilePath = 'C:/Users/mattx/Downloads/data/data/model.pkl'):

    """
    Input: pickleFilePath: string(must be valid filepath), dataFilePath: string(must be valid filepath)
    Output: pickle object 

    #INSERT THE PROPER FILEPATHS WHEN SETTING UP
    #MAKE SURE THE PICKLE FILE SAVES TO THE SAME FOLDER AS THIS FILE
    """

    #checking for pickle of model
    if os.path.isfile(pickleFilePath):

        with open(pickleFilePath, "rb") as f:
            pkl = pickle.load(f)

    else:

        #data for model
        df = pd.read_csv(dataFilePath, keep_default_na=True, delimiter=',', skipinitialspace=True)


        #Training model on full data, as performance has already been evaluated
        xgb_x_train = df[['day', 'month', 'week', 'hour', 'temp', 'feels_like', 'weather_main', 'taxi_zone']]
        xgb_y_train = df['activity']

        #Genrating the model
        #creating xgboost regression models
        dtrain_reg = xgb.DMatrix(xgb_x_train, xgb_y_train, enable_categorical=True)

        #defining parameters and training
        params = {"objective": "reg:squarederror", "tree_method": "gpu_hist"}
        n = 10000
                
        model = xgb.train(
        params=params,
        dtrain=dtrain_reg,
        num_boost_round=n,
        )

        #Pickling the model
        with open(pickleFilePath, "wb") as f:
            pickle.dump(model, f)

        with open(pickleFilePath, "rb") as f:
            pkl = pickle.load(f)

        
    print(pkl)

    #closing pickle file
    f.close()

    return pkl


#fetches the data from the postgreSQL
def fetch_data():

    """
    input: none
    output: pandas dataframe
    """



    return 0


#creates a new database to hold results
def create_db():

    """
    input: none
    output: none
    """

    

    return 0


#main function to be called by back-end
def machine_learn(pkl = pickle_load()):

    """
    Input: pickle file, 
    Output: results
    """


    return 0 


c = machine_learn()
