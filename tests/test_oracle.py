""" Test for oracle functions """
# pylint: disable=redefined-outer-name,unused-argument,unused-import
import json
from unittest.mock import patch
import azure.functions as func
from tests.fixtures import mock_env_access_key
from shared_code import oracle

@patch("shared_code.oracle.oracledb.connect")
def test_get_oracle_connection(mock_oracledb_connect, mock_env_access_key):
    """ test get orcale connection """
    mock_oracledb_connect.return_value = True
    assert oracle.get_oracle_connection()
