# This application takes an image and gives us the color palette as an output
# Based on https://towardsdatascience.com/image-color-extraction-with-python-in-4-steps-8d9370d9216e

import pandas as pd
import extcolors
from colormap import rgb2hex


def img_load(filepath='C:\\Users\\mattx\\Downloads\\manhattan.jpg'):

    """
    Args: filepath (String, valid file path)
    Returns: Extcolors object
    """

    color_palette = extcolors.extract_from_path(filepath, tolerance=12, limit=11)
    return color_palette

def palette_check(input=img_load()):

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
    return df

df = palette_check()
df.to_csv('color_palette', index=False)
