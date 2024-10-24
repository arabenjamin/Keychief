import pytest, os
from keychief.manager import PasswordManager

class TestManager:

    def test_manager_init_no_GPGKey(self):
        assert False

    def test_manager_init_no_git(self):
        assert False

    def test_manager_init_happy_path(self):
        assert False
    
    def test_store_dir_exists(self, temp_path):
        manager = PasswordManager(temp_path)
        assert os.path.exists(temp_path)
        