import pytest, os, uuid
from keychief.manager import PasswordManager, Options, DependacyError

class TestManager:


    def test_manager_GnupgHome(self, mock_gnupghome):
        
        options = Options(
            gnupg_home_dir = "$HOME/.mock_gnupg_home"
        )
        manager = PasswordManager(options=options)

        assert manager.ok
    
    def test_manager_GnupgNotHome(self):
        assert False

    def test_manager_init_GPGKey(self):
        assert False

    def test_manager_init_no_GPGKey(self):
        assert False

    def test_manager_init_git(self):
        assert False

    def test_manager_init_no_git(self):
        assert False



    def test_manager_init_happy_path(self):

        #with pytest.raises(DependacyError):
        #    PasswordManager()
        try:
            PasswordManager()
            assert True
        except DependacyError:
            assert False
        
    @pytest.mark.skip(reason=" Needs refactoring")
    def test_store_dir_exists(self, temp_path):
        manager = PasswordManager(password_store_dir = temp_path)
        assert os.path.exists(temp_path)

    @pytest.mark.skip(reason=" Need automatic passphrase for key, need to mock key")
    def test_add_password(self, temp_path, fake_password):
        fake_secret = "Notmysecret"
        manager = PasswordManager(password_store_dir = temp_path)
        
        secret = manager.add_password(fake_secret,fake_password)
        assert secret.ok
    
    
    @pytest.mark.skip(reason=" Need automatic passphrase for key, need to mock key")
    def test_get_passowrd(self, temp_path, fake_password):
        fake_secret = "Notmysecret"
        manager = PasswordManager(password_store_dir = temp_path)
        strored_secret = manager.add_password(fake_secret,fake_password)
        retrieved_password = manager.get_password(fake_secret)
        assert retrieved_password.ok
        assert retrieved_password.data == fake_secret
        
    @pytest.mark.skip(reason=" Need automatic passphrase for key, need to mock key")
    def test_list_passwords(self, temp_path, fake_password):
        fake_secret = "Notmysecret"
        manager = PasswordManager(password_store_dir = temp_path)
        strored_secret = manager.add_password(fake_secret,fake_password)
        assert len(manager.list_passwords() ) == 1
    
 