import pandas as pd
from D2Ltools import extract_D2L_assigns, extract_D2L_usernames
from D2Ltools import extract_D2L_OrgIDs
from wptools import extract_wp_assigns, extract_wp_names
from fuzzytools import match_list
from gooey import Gooey
from gooey import GooeyParser

def convert_grades(wp='wp_download.csv', D2L='D2L_download.csv'):
    """
    This function takes in a WileyPlus .csv download of student grades along with a download of D2L grades
    It then outputs a pandas dataframe in the format that D2L can read.
    output dataframe needs to be converted to a .csv before uploading to D2L
    :param wp: .csv download from WileyPlus. Full file path including .csv extension
    :param D2L: .csv download from D2L. Full file path including .csv extension
    :return: df, pandas dataframe formatted for D2L
    """
    wp_csv = wp
    D2L_csv = D2L

    # read in D2L csv as pandas df, make a list of D2L Usernames
    df2 = pd.read_csv(D2L_csv)
    d2l_username_lst = df2['Username'].tolist()

    # read in WileyPlus csv as pandas df, skip last line which has totals instead of a student name
    # Insert a new column that combines First and Last names to make one name with a space
    # make a list of these WileyPlus full names
    df = pd.read_csv(wp_csv, skipinitialspace=True, skipfooter=1, engine='python')
    df.insert(0, 'wp_name', df['First Name'] + ' ' + df['Last Name'])
    wp_name_lst = df['wp_name'].tolist()

    # make a dict with {Keys: 'WileyPlus Full Names', Values:'D2L Usernames'}
    wpname2d2lusername_dict = match_list(wp_name_lst, d2l_username_lst)

    # insert a new column in WileyPlus df with D2L Usernames mapped from WileyPlus full names
    # using dict with {Keys: 'WileyPlus Full Names', Values:'D2L Usernames'}
    df.insert(0, 'Username', df['wp_name'].map(wpname2d2lusername_dict))

    # make a dict of {Keys: 'D2L Usernames', Values: 'D2L OrgDefinedIds'}
    d2l_username_to_orgid_dict = dict(zip(df2['Username'], df2['OrgDefinedId']))
    # insert in a new first column in WileyPlus df with D2L OrgDefinedIds mapped from D2L Usernames
    # using dict with {Keys: 'D2L Usernames', Values: 'D2L OrgDefinedIds'}
    df.insert(0, 'OrgDefinedId', df['Username'].map(d2l_username_to_orgid_dict))

    # remove hash(#) signs, drop columns that aren't grades, drop columns with stars(*)
    df['OrgDefinedId'] = df['OrgDefinedId'].map(lambda x: x.lstrip('#'))
    df['Username'] = df['Username'].map(lambda x: x.lstrip('#'))
    cols_to_drop_lst = ['wp_name', 'First Name', 'Last Name', 'Email', 'Course name', 'Class-section name', 'Date', 'Overall Score (%)']
    df.drop(cols_to_drop_lst, axis=1, inplace=True)
    col_name_lst = df.columns.values.tolist()
    cols_with_star_lst = [c for c in col_name_lst if '*' in c]
    df.drop(cols_with_star_lst, axis=1, inplace=True)

    # get list of WileyPlus and D2L assignments, them match them up in a
    # dict of {Keys: 'WileyPlus Assigns': Values:'D2L Assigns'}
    d2l_assings_lst = extract_D2L_assigns(D2L_csv)
    wp_assigns_lst = extract_wp_assigns(wp_csv)
    wpassigns2d2lassigns_dict = match_list(wp_assigns_lst, d2l_assings_lst)

    # use dict of WileyPlus and D2L Assigns to rename columns with D2L assign names
    df.rename(columns=wpassigns2d2lassigns_dict, inplace=True)

    # Take out blanks, Grades not released and Not assigned entries
    df = df.replace('Grades Not Released', ' ', regex=True)  # remove all Grades not replaced cells
    df = df.replace('Not Assigned', ' ', regex=True)  # remove all not assigned marks
    df = df.fillna('')
    df['End-of-Line Indicator'] = '#'  # add a column with End-of-Line Indicator # needed by D2L

    df.set_index('OrgDefinedId', drop=True, inplace=True) # set first column as D2L OrgDefinedId's

    #Now the dataframe should be ready to go. Just print out to make sure.
    print(df)
    return(df)

@Gooey
def main(wp='wp_download.csv', D2L='D2L_download.csv', output='output.csv'):
    parser = GooeyParser(description="Grade Conversion GUI App!")
    parser.add_argument('WileyPlus_csv', help="Browse to the WileyPlus file you downloaded", widget='FileChooser')
    parser.add_argument('D2L_csv', help="Browse to the D2L file you downloaded", widget='FileChooser')
    parser.add_argument('output_csv', help="Type name of output csv file, include .csv extension", widget='TextField')
    args = vars(parser.parse_args())

    wp_csv = (args["WileyPlus_csv"])
    D2L_csv = (args["D2L_csv"])
    output_csv = (args["output_csv"])

    # big function that creates the pandas dataframe in the D2L grade format with all the WileyPlus Grades
    out_df = convert_grades(wp_csv, D2L_csv)
    print('\n Output dataframe created successfully \n ')

    # write the output dataframe to  csv
    out_df.to_csv(output_csv)

    print('Success! Output is in current folder and named: ')
    print(output_csv)

if __name__ == "__main__":
    main()
