
import pandas as pd
import numpy as np
from fuzzytools import printDict


#import D2L csv and get list of usernames
def extract_D2L_usernames(D2L_csv):
    df = pd.read_csv(D2L_csv)
    pdnames = df['Username']  #pull the usernames into a pd dataframe
    D2L_names = pdnames.tolist() #convert pd dataframe to regular list
    D2L_usernames = [s.strip('#') for s in D2L_names] #remove the # in the name
    print('D2L Names = ', D2L_usernames)
    return(D2L_usernames)


#import D2L csv and form dictionary from OrgID and UserNames
def extract_D2L_OrgIDs(D2L_csv):
    df = pd.read_csv(D2L_csv, skipinitialspace=True)
    #print(df)
    OrgIDd={}
    UN = df['Username']
    #print(UN)
    Users = UN.tolist()  # convert pd dataframe to regular list
    Usernames = [s.strip('#') for s in Users]  # remove the # in the name
    #print('D2L Usernames = ', Usernames)

    ID = df['OrgDefinedId']
    #print(ID)
    IDs = ID.tolist()  # convert pd dataframe to regular list
    OrgIDs = [x.strip('#') for x in IDs]  # remove the # in the name
    #OrgIDs=['G03460796', 'G03219671', 'G02983595']
    #print( 'D2L OrgIDs = ', OrgIDs)
    OrgIDd = dict(zip(Usernames, OrgIDs))
    printDict(OrgIDd)

    return(OrgIDd)


#import D2L csv and get list of assignments
def extract_D2L_assigns(D2L_csv):
    dg = pd.read_csv(D2L_csv)
    column_headers = dg.columns.values.tolist()
    print('D2L column headers = ', column_headers)
    D2L_assigns_with_details = [x for x in column_headers if "Points Grade" in x]
    D2L_assigns=[]
    for s in D2L_assigns_with_details:
        stripped = s.split("<")[0]
        D2L_assigns.append(stripped)
    print('D2L assignments =', D2L_assigns)
    return(D2L_assigns)


def main():
    csv='D2L_download.csv'
    extract_D2L_usernames(csv)
    extract_D2L_OrgIDs(csv)
    extract_D2L_assigns(csv)


if __name__ == "__main__":
    main()