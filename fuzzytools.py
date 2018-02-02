from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# this function matches the items in one list to the items in another
# the input list must be shorter or the same length as the output list
# the input list becomes the dictionary key
# the master list becomes the linked items

def match_list(input_list,master):
    dict = {}
    for item in input_list:
        match = process.extractOne(item, master)
        dict[item] = match[0]
        print(item,' = ',match[0],'     % match =', match[1])
    #print(dict)
    return dict

def printDict(d):
    for entry in d:
        print(entry, ' : ', d[entry])
