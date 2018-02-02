from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
from fuzzytools import match_list
import numpy as np
import math

def extract_wp_names(wp_csv):
    df = pd.read_csv(wp_csv)
    #print(df)
    df['Name'] = df['First Name'] + ' ' + df['Last Name'] #Combine first and last name
    #print(df)
    name_list = df['Name']
    #print(name_list)
    #print(type(name_list))
    names_with_spaces=name_list.tolist()
    #print(names_with_spaces, type(names_with_spaces))
    wp_names_with_spaces = [x for x in names_with_spaces if str(x) != 'nan'] # take out NaN
    wp_names=[s.strip() for s in wp_names_with_spaces] # take out spaces
    if 'Total Points Available' in wp_names: wp_names.remove('Total Points Available')
    #print('WileyPlus Names =', wp_names)
    return(wp_names)

#import wp csv and get list of assignments
def extract_wp_assigns(wp_csv):
    df = pd.read_csv(wp_csv)
    column_headers = df.columns.values.tolist()
    #print(column_headers)
    wp_assigns= column_headers[7:]
    wp_assigns = [a for a in wp_assigns if '*' not in a] #remove *assignments
    #print(wp_assigns)
    return(wp_assigns)