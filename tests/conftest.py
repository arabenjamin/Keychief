import uuid 
import pytest, gnupg
from git import Repo

from keychief.manager import Result, PasswordManager


class MockGPG:
    """Create a mock GPG object."""
    def encrypt(self, data, recipients=None, symmetric=True):
        print(f"\nEncrypting data {data}...\n")
        return Result(
            ok = True,
            data = str(f"ENCRYPTED_{data}")
        )

    def decrypt(self, data):
        print(f"Decrypting data {data}")
        decrypted = data.replace("ENCRYPTED_", "")
        return Result(
            ok = True,
            data = decrypted
        )

    @staticmethod
    def list_keys(secretkey:bool):
        return [{"SECRETKEY":"SECRETVALUE"}]


@pytest.fixture(autouse=True)
def mock_gpg(monkeypatch):
    
    def mockencrypt(*args, **kwargs):
        return MockGPG()  

    monkeypatch.setattr("gnupg.GPG", mockencrypt)


@pytest.fixture
def mock_git_repo(temp_dir):
    """Create a mock Git repository."""
    repo = Repo.init(temp_dir)
    return repo


# NOTE/TODO : This is probably just poor form and should be rethought
@pytest.fixture
def temp_key():
    # We need to generate temp keys and passphases on the fly \
    # so we dont need to use our GPGkey, or passphrase
    gpg = gnupg.GPG()
    key = gpg.gen_key(gpg.gen_key_input())
    yield key
    gpg.delete_keys(key.fingerprint, True)
    gpg.delete_keys(key.fingerprint)


@pytest.fixture
def fake_password():
    yield str(uuid.uuid4())

