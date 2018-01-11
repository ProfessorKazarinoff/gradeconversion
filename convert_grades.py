import argparse
import pandas as pd
import numpy as np
import math
from D2Ltools import extract_D2L_assigns, extract_D2L_usernames
from D2Ltools import extract_D2L_OrgIDs
from wptools import extract_wp_assigns, extract_wp_names
from fuzzytools import match_list

# construct the argument parse and parse the arguments
# -i followed by the WileyPlus csv
# -r followed by the D2L csv
# -o followed by the name of the output csv
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--WileyPlus", required=True,
	help="path to the WileyPlus_Grades .csv file")
ap.add_argument("-r", "--D2L",
	help="path to cat detector haar cascade")
ap.add_argument("-o", "--output",
	default="output.csv",
	help="path to output .csv file")
args = vars(ap.parse_args())



# load the input image and convert it to grayscale
wp_csv=(args["WileyPlus"])
D2L_csv=(args["D2L"])
output_csv=(args["output"])

def main():

    # match names for WP and D2L in a dict
    wp_names = extract_wp_names(wp_csv)
    D2L_names = extract_D2L_usernames(D2L_csv)
    named = match_list(wp_names, D2L_names)

    # create a dict with the D2L OrgID's and D2L names
    UserIDdict = extract_D2L_OrgIDs(D2L_csv)

    # match assignments for WP and D2L and in a dict
    D2L_assigns = extract_D2L_assigns(D2L_csv)
    wp_assigns = extract_wp_assigns(wp_csv)
    assignd = match_list(wp_assigns, D2L_assigns)

    # read in the WP csv download, convert to Pandas Dataframe. Used to build grade sheet
    df = pd.read_csv(wp_csv, skipinitialspace=True, skipfooter=2) # last two lines contain total points
    #print(df) #combine first and last name into a new column at the end
    df['endUsername'] = df['First Name'] + ' ' + df['Last Name']  # Combine first and last name
    #print(df)
    # replace the WP names with the D2L names
    df['endUsername'].replace(named, inplace=True)
    # replace the WP assignments with the D2L assignments
    df = df.rename(columns=assignd)
    df.drop(df.columns[[0, 1, 2, 3, 4, 5, 6]], axis=1, inplace=True) # get rid of the first 7 collumns which don't contain grades

    # put the Username column first
    df.insert(0, 'Username', df['endUsername'])
    df.drop('endUsername', axis=1, inplace=True)

    # insert of column of the D2L OrgID's
    df.insert(0, 'OrgDefinedId', df['Username'].map(UserIDdict))
    df.set_index('OrgDefinedId', drop=True, inplace=True)

    df = df.replace('Grades Not Released', ' ', regex=True) #remove all Grades not replaced cells
    df = df.fillna('') #fill any NaN cells

    df['End-of-Line Indicator'] = '#' #add a collumn with End-of-Line Indicator # needed by D2L
    print(df)

    df.to_csv(output_csv)

if __name__ == "__main__":
    main()




