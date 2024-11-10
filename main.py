import sys
import argparse
from keychief.install import install
from keychief.manager import PasswordManager, DependacyError


def main():
    password_store_dir = "~/.password-store"
   
    try:
        manager = PasswordManager(password_store_dir)
        manager.init_password_store()
    except DependacyError as e:
        print(e) # we should probably do something else here


    # TODO: Better management of cmdline args 
    if len(sys.argv) < 2:
        print("Usage: password_manager.py [add|get|list] [name] [password]")
        sys.exit(1)

    command = sys.argv[1]


     


def main_with_argparse():
    print("Welcome to KeyChief!\nThe Chief of keys")

    parser = argparse.ArgumentParser(
        prog='KeyChief',
        description="Welcome to KeyChief",
        epilog="Inspired by Pass Pass the standard Unix password manager and \
            KeyPass that no longer exists")
    
    parser.add_argument('path', help='pathname for where to keep passwords')
    
    parser.add_argument('list', help='list the logins we have passwords for, \
                        not the passwords themselves')


    parser.add_argument('show', help='Show the password for that login')

    parser.add_argument('create_new', help='Store new password')

    args = parser.parse_args()
    if args.init:
        install(args.init)

if __name__ == "__main__":


    #main()
    print("Welcome to KeyChief!\nThe Chief of keys")


    password_store_dir = "~/.password-store"
    
    try:
        manager = PasswordManager(password_store_dir)
        manager.init_password_store()
    except DependacyError as e:
        print(e) # we should probably do something else here

    #TODO: Work In Progress ....
    parser = argparse.ArgumentParser(
        prog='KeyChief',
        description="Welcome to KeyChief",
        epilog="Inspired by Pass Pass the standard Unix password manager and \
            KeyPass that no longer exists")
    
    parser.add_argument('path', help='pathname for where to keep passwords')
    
    parser.add_argument('list', help='list the logins we have passwords for, \
                        not the passwords themselves')


    parser.add_argument('show', help='Show the password for that login')

    parser.add_argument('create_new', help='Store new password')

    args = parser.parse_args()

    match args:

        case "add":
            manager.add_password(sys.argv[2], sys.argv[3])
            print(f"Password for {sys.argv[2]} added successfully.")
        case "show":
            password = manager.get_password(sys.argv[2])
            if password:
                print(f"Password for {sys.argv[2]}: {password}")
            else:
                print(f"No password found for {sys.argv[2]}")
        case "list":
            passwords = manager.list_passwords()
            print("Stored passwords:")
            for password in passwords:
                print(password)
        case _:
            print("Please see help")
            sys.exit(1)