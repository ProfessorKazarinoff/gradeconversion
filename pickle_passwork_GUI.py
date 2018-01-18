import pickle
from gooey import Gooey, GooeyParser
import pprint

@Gooey
def main():
    parser = GooeyParser(description="Password Pickling App")
    parser.add_argument('Username', help="Enter Username to store", widget='TextField')
    parser.add_argument('Password', help="Enter password to store", widget='TextField')
    args = vars(parser.parse_args())
    username = args['Username']
    password = args['Password']

    passcode_dict = {'UserName':username,'Password':password}

    pickling_on = open("passcode_dict.pickle","wb")
    pickle.dump(passcode_dict, pickling_on)
    pickling_on.close()

    pickle_off = open("passcode_dict.pickle","rb")
    converted_dict = pickle.load(pickle_off)
    pprint.pprint(converted_dict)


if __name__ == '__main__':
    main()