import pickle
from gooey import Gooey, GooeyParser
import os

@Gooey
def main():
    parser = GooeyParser(description="Password Pickling App")
    parser.add_argument('Username', help="Enter Username to store", widget='TextField')
    parser.add_argument('Password', help="Enter password to store", widget='TextField')
    args = vars(parser.parse_args())
    username = args['Username']
    password = args['Password']

    passcode_dict = {'UserName':username,'Password':password}

    #make sure there is a .config directory and create one if there is not
    if not os.path.exists('.config'):
        print('Making .config directory....')
        os.mkdir('.config')
    if os.path.exists('.config'):
        print('.config directory exists')



    #define .config directory
    os.getcwd()
    print('current directory is: ')
    print(os.getcwd())
    basedir = os.getcwd()
    configdir = os.path.join(basedir, '.config')
    print('.config directory is: ')
    print(configdir)

    #pickle the password dict
    pickling_on = open(os.path.join(configdir, 'passcode_dict.pickle'), "wb")
    pickle.dump(passcode_dict, pickling_on)
    pickling_on.close()

    #confirm .pickle file is in the .config directory
    print('pickled password dict saved in .config/ as:')
    print(os.listdir(configdir))

    #pull the pickle out, unpickle and print to the REPL
    pickle_off = open(os.path.join(configdir, 'passcode_dict.pickle'), "rb")
    converted_dict = pickle.load(pickle_off)
    print('unpickled password dict: ')
    print(converted_dict)


if __name__ == '__main__':
    main()