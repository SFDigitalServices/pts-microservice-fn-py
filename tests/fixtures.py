""" Test fixtures """
from unittest.mock import Mock
import pytest

CLIENT_HEADERS = {
    "ACCESS_KEY": "1234567"
}

@pytest.fixture
def mock_env_access_key(monkeypatch):
    """ mock environment access key """
    monkeypatch.setenv("ACCESS_KEY", CLIENT_HEADERS["ACCESS_KEY"])
    monkeypatch.setenv("PTS_USERNAME", "test")
    monkeypatch.setenv("PTS_PASSWORD", "test")
    monkeypatch.setenv("PTS_CONNECTSTRING", "127.0.0.1:1111/DB")
    monkeypatch.setenv("ORACLE_LIB_DIR", "./lib/instantclient_19_8")
    monkeypatch.setenv("LD_LIBRARY_PATH", "")

@pytest.fixture
def mock_env_no_access_key(monkeypatch):
    """ mock environment with no access key """
    monkeypatch.delenv("ACCESS_KEY", raising=False)

def mock_cursor(val):
    """ mocking cursor """
    cursor = Mock()
    cursor.getvalue.return_value = val
    return cursor
