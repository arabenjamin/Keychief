#!/usr/bin/env python3

import os, sys, logging
import gnupg, git
from typing import Optional


class NoGpgKeyError(Exception):
    """ No GpgKey found """
    pass



class PasswordManager:

    """ 
    Inspiration:
        Password manager in python, using git and Gpg2 
        built to be interchangeable with Pass the standard Unix password manager.
        
    Reference: 
        https://gnupg.readthedocs.io/en/stable/
        https://gitpython.readthedocs.io/en/stable/

    """

    def __init__(self, password_store_dir: Optional[str] = None) -> None:
        

        # NOTE: this should probably follow the best practices from the documentation
        # add in a path to this call
        self.gpg = gnupg.GPG() # path/to/.gnupg

        # we need to create a gpgkey or peace out  
        if self.check_for_gpgkey() is not True:  
            # for now we'll tell the user to either create one themselves or fuck off
            raise NoGpgKeyError("No GpgKey present. Either import a key or create a new one")
        
        self.password_store_dir = "~/.password-store"
        # If the password_store_dir is being passed in
        # we're makeing an assumtion that the password store
        # is being created for the first time.
        if self.password_store_dir is not None:
            self.password_store_dir = os.path.expanduser(password_store_dir)
            self.init_password_store()
           
        self.repo = git.Repo(self.password_store_dir)

        
    def check_for_gpgkey(self) -> bool:
        # NOTE: In future it may be useful to pic
        # a key if there is more than one.
        # For now we're assuming there's only one key present 
        if len(self.gpg.list_keys()) > 0:
            return True
        return False

    def init_password_store(self) -> None:
        
        os.makedirs(self.password_store_dir, exist_ok=True)
        if not os.path.exists(os.path.join(self.password_store_dir, '.git')):
            git.Repo.init(self.password_store_dir)



    def add_password(self, name, password):
        encrypted_password = self.gpg.encrypt(password, recipients=None, symmetric=True)
        file_path = os.path.join(self.password_store_dir, f"{name}.gpg")
        with open(file_path, 'wb') as f:
            f.write(str(encrypted_password).encode('utf-8'))
        self.repo.index.add([file_path])
        self.repo.index.commit(f"Add password for {name}")

    def get_password(self, name):
        file_path = os.path.join(self.password_store_dir, f"{name}.gpg")
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'rb') as f:
            encrypted_password = f.read()
        decrypted_password = self.gpg.decrypt(encrypted_password)
        return str(decrypted_password)

    def list_passwords(self):
        passwords = []
        for root, dirs, files in os.walk(self.password_store_dir):
            for file in files:
                if file.endswith('.gpg'):
                    passwords.append(os.path.splitext(file)[0])
        return passwords



    def create_new_key(self) -> str:
        # create a new gpg key return the fingerprint
        return None

    def list_keys(self) -> list:
        return []

    def import_key(self, key:str) -> None:
        return None
    