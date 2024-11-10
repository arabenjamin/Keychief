#!/usr/bin/env python3

import os, sys, logging, subprocess
import gnupg, git
from pydantic import BaseModel
from typing import Optional
from enum import Enum



class Dependacy(Enum):
    # TODO: This is wrong and needs to be rethought
    GIT = "git"
    GPG = "gpg"


class Result(BaseModel):
    data: Optional[str] = None
    ok: bool
    error: Optional[Exception] = None
    

class Options(BaseModel):
    password_store_dir: Optional[str] = "~/.password-store"
    gnupg_home_dir:Optional[str] = "~/.gnupg"
    key_fingerprint: Optional[str] = None
    with_git: bool
    repo_path: Optional[str] = "~/.password-store/.git" 
    # TODO : Add default validation
    

class DependacyError(Exception):
    """ Missing a Dependacy"""

class InitGPGFailureError(Exception):
    """Gpg failed to inialize"""
    pass

class NoGpgKeyError(Exception):
    """ No GpgKey found """
    pass



class PasswordManager:

    """ 
    Inspiration:
        Password manager in python, using git and Gpg2 
        built to be interchangeable with Pass the standard Unix password manager.
        https://www.passwordstore.org/
        
        
    Reference: 
        https://gnupg.readthedocs.io/en/stable/
        https://gitpython.readthedocs.io/en/stable/

    """

    def __init__(self, options: Options) -> None:
        

        self.options: Options = options
        self.ok: bool = False

        # Check and make sure our depancies are installed
        if not self.__IsDependancyInstalled("git"):

            raise DependacyError(f"Missing Dependacy, {Dependacy.GIT} must be installed")
        
        if not self.__IsDependancyInstalled("gpg"):
            raise DependacyError(f"Missing Dependacy, {Dependacy.GPG} must be installed")

        # Setup Gpg
        if not self.__initGpg():
            raise InitGPGFailureError("Failed to initiate Gpg")

        # TODO: we need to create a gpgkey or peace out  
        if self.__check_for_gpgkey() is not True:  
            # for now we'll tell the user to either create one themselves or fuck off
            raise NoGpgKeyError("No GpgKey present. Either import a key or create a new one")
 

        # Setup the directory for our password store
        if not os.path.exists(self.options.password_store_dir):
            # create the directory, and set in config file TODO: set config
            password_store_dir = os.path.expanduser(self.options.password_store_dir)
            os.makedirs(password_store_dir, exist_ok=True)

        # set up git
        # TODO: Add ability to clone from exisiting repo
        # check if a git repo exists, create it if not
        if os.path.exists(self.options.repo_path):
            self.repo = git.Repo(self.options.password_store_dir)
        else:
            self.repo = git.Repo.init(self.options.password_store_dir)
        
        self.ok = True


    def __IsDependancyInstalled(self, dependacy:Dependacy) -> bool:

        try:
            subprocess.run([f"{dependacy}", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def __initGpg(self) -> bool:
        # set up GPG
        try:
            self.gpg = gnupg.GPG(gnupghome=os.path.expanduser(self.options.gnupg_home_dir))
            return True
        except ValueError as e:
            # Presumably the path isnt there
            os.mkdir(os.path.expanduser(self.options.gnupg_home_dir))
            self.gpg = gnupg.GPG(gnupghome=os.path.expanduser(self.options.gnupg_home_dir))
            return True

        


    def __check_for_gpgkey(self) -> bool:
        # NOTE: In future it may be useful to pic
        # a key if there is more than one.
        # For now we're assuming there's only one key present
        #  
        if len(self.gpg.list_keys(True)) > 0:
            return True
        return False


    def add_password(self, secret:str, password:str) -> Result:
        encrypted_password = self.gpg.encrypt(password, recipients=None, symmetric=True)
        if not encrypted_password.ok:
            return Result(
                error = encrypted_password.status,
                ok = encrypted_password.ok
            )

        file_path = os.path.join(self.password_store_dir, f"{secret}.gpg")
        with open(file_path, 'wb') as f:
            f.write(str(encrypted_password.data).encode('utf-8'))
        #self.repo.index.add([file_path])
        #self.repo.index.commit(f"Add password for {secret}")
        return Result(
            data = encrypted_password.status,
            ok = encrypted_password.ok
        )

    def get_password(self, secret:str):

        file_path = os.path.join(self.password_store_dir, f"{secret}.gpg")
        if not os.path.exists(file_path):
            return Result(
                error = "File not found",
                ok = False
            )
        
        
        with open(file_path, 'rb') as f:
            encrypted_password = f.read()
        decrypted_password = self.gpg.decrypt(encrypted_password)
        
        return Result(
            data = decrypted_password,
            ok = decrypted_password.ok
        )

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
    