import pytest
import os, uuid
import shutil
import gnupg
from pathlib import Path





@pytest.fixture
def mock_gnupghome(monkeypatch):
    def mock_home(*args, **kwargs):
        return Path("$HOME/.test_gnupghome")
    monkeypatch.setattr(Path, "$HOME/.gnugpg", mock_home)


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




# TODO: tmp_path is a built in fixture in pytest and should be used here.
@pytest.fixture
def temp_path():
    tempath = "$HOME/.test_password_store"
    yield tempath
    shutil.rmtree(tempath)

@pytest.fixture
def fake_password():
    yield str(uuid.uuid4())

