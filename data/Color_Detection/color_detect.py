# This application takes an image and gives us the color palette as an output
# Based on https://towardsdatascience.com/image-color-extraction-with-python-in-4-steps-8d9370d9216e

import numpy as np
import pandas as pd
import extcolors
from colormap import rgb2hex
from sqlalchemy import create_engine, URL
import json
import geojson
import requests
from PIL import Image
from io import BytesIO
from credentials import pg_conn



#loads in the image and extracts a basic RGB color palette
def img_load(url):

    """
    Args: filepath (String, valid file path)
    Returns: Extcolors object
    """

    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    color_palette = extcolors.extract_from_image(image, tolerance=12, limit=11)
    return color_palette 



#takes the RGB color palette and converts it to a dataframe of hex values, along with the frequency
def palette_check(input):

    """
    Args: input (Extcolors object)
    Returns: Hex code occurence df (Pandas dataframe)
    """

    colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
    
    #convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")), int(i.split(", ")[1]), int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
    
    df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
    return df['c_code'].to_list()



#opens the geojson file with the taxi zone images, and populates the df with color frequencies
def open_geo(geojson='C:\\Users\\mattx\\Downloads\\cityframe-1\\data\\Color_Detection\\zones_with_images.geojson'):
    
    """
    Args: Geojson File (containing taxi zones/ flickr image links)
    Returns: Pandas dataframe
    """

    with open(geojson, 'r') as f:
        data = json.load(f)
    
    zones = []
    image_urls = []
    colors = []


    features = data['features']

    for feature in features:

        properties = feature['properties']
        zones.append(properties['zone'])
        image_urls.append(properties['image_url'])

        image = img_load(properties['image_url'])
        colors.append(palette_check(image))

    df = pd.DataFrame({'zone': zones, 'image_url': image_urls, 'colors': colors})
    return df



# creates a new database to hold results
def create_db(self, df):

    """
    Args: pandas dataframe
    Returns: None
    """

    engine = create_engine(self.pg_url)

    df.to_sql('Color_Results', engine, schema='cityframe', if_exists='replace', index=False)

    return None



df = create_db(open_geo())