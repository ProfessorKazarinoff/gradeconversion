
import pandas as pd
from D2Ltools import extract_D2L_assigns, extract_D2L_usernames
from D2Ltools import extract_D2L_OrgIDs
from wptools import extract_wp_assigns, extract_wp_names
from fuzzytools import match_list
from gooey import Gooey
from gooey import GooeyParser


def convert_grades(wp='wp_download.csv', D2L='D2L_download.csv', output='output.csv'):
    # define the WileyPlus, D2L and output csv objects
    wp_csv = wp
    D2L_csv = D2L
    output_csv = output

    # match names for WP and D2L in a dict
    wp_names = extract_wp_names(wp_csv)   #wp_names is a list, with 'Frist Last' entries
    D2L_names = extract_D2L_usernames(D2L_csv) #D2L names is a list, with 'first.last2'
    named = match_list(wp_names, D2L_names) #named is a dict with Key:'First Last' value: 'first.last2'

    # create a dict with the D2L OrgID's and D2L names
    UserIDdict = extract_D2L_OrgIDs(D2L_csv) #UserIDdict is a dict with Key: 'first.last2' value: 'G03423334'

    # match assignments for WP and D2L and in a dict
    D2L_assigns = extract_D2L_assigns(D2L_csv)
    wp_assigns = extract_wp_assigns(wp_csv)
    assignd = match_list(wp_assigns, D2L_assigns)

    # read in the WP csv download, convert to Pandas Dataframe. Used to build grade sheet
    df = pd.read_csv(wp_csv, skipinitialspace=True, skipfooter=2,
                     engine='python')  # last two lines contain total points
    # print(df) #combine first and last name into a new column at the end
    df['endUsername'] = df['First Name'] + ' ' + df['Last Name']  # Combine first and last name
    #print(df)
    # replace the WP names with the D2L names
    df['endUsername'].replace(named, inplace=True)
    #print(df)
    # replace the WP assignments with the D2L assignments
    df = df.rename(columns=assignd)
    #print(df)
    df.drop(df.columns[[0, 1, 2, 3, 4, 5, 6]], axis=1, inplace=True)  # get rid of the first 7 columns which don't contain grades

    # put the Username column first
    df.insert(0, 'Username', df['endUsername'])
    df.drop('endUsername', axis=1, inplace=True)
    print(df)

    # insert of column of the D2L OrgID's
    df.insert(0, 'OrgDefinedId', df['Username'].map(UserIDdict))
    df.set_index('OrgDefinedId', drop=True, inplace=True)
    print(df)
    df = df.replace('Grades Not Released', ' ', regex=True)  # remove all Grades not replaced cells
    df = df.replace('Not Assigned', ' ', regex=True) # remove all not assigned marks
    df = df.fillna('')  # fill any NaN cells

    df['End-of-Line Indicator'] = '#'  # add a column with End-of-Line Indicator # needed by D2L
    #print(df)

    # write the output csv
    df.to_csv(output_csv)

@Gooey
def main():
    parser = GooeyParser(description="Grade Conversion GUI App!")
    parser.add_argument('WileyPlus_csv', help="Browse to the WileyPlus file you downloaded", widget='FileChooser')
    parser.add_argument('D2L_csv', help="Browse to the D2L file you downloaded", widget='FileChooser')
    parser.add_argument('output_csv', help="Type name of output csv file, include .csv extension", widget='TextField')
    args = vars(parser.parse_args())

    wp_csv = (args["WileyPlus_csv"])
    D2L_csv = (args["D2L_csv"])
    output_csv = (args["output_csv"])

    convert_grades(wp_csv,D2L_csv,output_csv)




if __name__ == "__main__":
    main()