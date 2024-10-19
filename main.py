import sys
import argparse
from keychief.install import install
from keychief.manager import PasswordManager

def main():
    password_store_dir = "~/.password-store"
    manager = PasswordManager(password_store_dir)
    manager.init_password_store()

    if len(sys.argv) < 2:
        print("Usage: password_manager.py [add|get|list] [name] [password]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add" and len(sys.argv) == 4:
        manager.add_password(sys.argv[2], sys.argv[3])
        print(f"Password for {sys.argv[2]} added successfully.")
    elif command == "get" and len(sys.argv) == 3:
        password = manager.get_password(sys.argv[2])
        if password:
            print(f"Password for {sys.argv[2]}: {password}")
        else:
            print(f"No password found for {sys.argv[2]}")
    elif command == "list":
        passwords = manager.list_passwords()
        print("Stored passwords:")
        for password in passwords:
            print(password)
    else:
        print("Invalid command or arguments.")
        sys.exit(1)


def main_with_argparse():
    print("Welcome to KeyChief!\nThe Chief of keys")

    parser = argparse.ArgumentParser(prog='KeyChief',description="Welcome to KeyChief")
    
    parser.add_argument('path', help='pathname for where to keep passwords')
    
    parser.add_argument('list', help='list the logins we have passwords for, \
                        not the passwords themselves')


    parser.add_argument('show', help='Show the password for that login')

    parser.add_argument('create_new', help='Store new password')

    args = parser.parse_args()
    if args.init:
        install(args.init)

if __name__ == "__main__":


    main()
    
