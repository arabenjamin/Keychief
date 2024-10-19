import pytest
import os

@pytest.fixture
def temp_path():
    tempath = "$HOME/.test_password_stor"
    yield tempath
    os.removedirs(tempath)