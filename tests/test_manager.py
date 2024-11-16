import pytest, os, uuid, logging
from keychief.manager import PasswordManager, Options, DependacyError

class TestManager:

    
    @pytest.mark.skip(reason="Still working out the bugs")
    def test_manager_init_no_GPGKey(self, ):
        """ without Key graceful fail """
        #with pytest.raises(DependacyError):
        #    PasswordManager()
        assert False

    @pytest.mark.skip(reason="Still working out the bugs")
    def test_manager_init_no_git(self):
        #with pytest.raises(DependacyError):
        #    manager = PasswordManager()
        
        assert False

    def test_manager_init_happy_path(self, tmp_path, caplog):

        #with pytest.raises(DependacyError):
        #    PasswordManager()

        try:
            
            options = Options(
                password_store_dir=str(tmp_path)
            )
            manager = PasswordManager(options = options)
            caplog.set_level(logging.INFO)
            assert manager.ok
        except DependacyError:
            assert False
 
    def test_store_dir_exists(self, tmp_path):
        options = Options(
            password_store_dir=str(tmp_path)
        )
        manager = PasswordManager(options = options)
        assert os.path.exists(manager.password_store_dir)

    def test_add_password(self, tmp_path, fake_password, mock_gpg, caplog):
        print("Mocking encrypt")

        fake_secret = "Notmysecret"
        options = Options(
            password_store_dir=str(tmp_path)
        )
        manager = PasswordManager(options = options)
        
        secret = manager.add_password(fake_secret,fake_password)

        assert secret.ok
        assert secret.data == f"ENCRYPTED_{fake_password}"

    def test_get_passowrd(self, tmp_path, fake_password, mock_gpg, caplog):
        fake_secret = "Notmysecret"

        options = Options(
            password_store_dir=str(tmp_path)
        )
        manager = PasswordManager(options = options)
        strored_secret = manager.add_password(fake_secret,fake_password)
        assert strored_secret.ok
        retrieved_password = manager.get_password(fake_secret)
        assert retrieved_password.ok
        assert str(retrieved_password.data) == fake_password
 
    def test_get_missing_password(self):
        assert False
    

    def test_list_passwords(self, tmp_path, fake_password, mock_gpg, caplog):
        fake_secret = "Notmysecret"
        options = Options(
            password_store_dir=str(tmp_path)
        )
        manager = PasswordManager(options = options)
        strored_secret = manager.add_password(fake_secret,fake_password)
        assert len(manager.list_passwords() ) == 1
    
 