""" Test for oracle functions """
# pylint: disable=redefined-outer-name,unused-argument,unused-import
import json
from unittest.mock import patch
import azure.functions as func
from tests.fixtures import mock_env_access_key
from shared_code import oracle

@patch("shared_code.oracle.oracledb.init_oracle_client")
@patch("shared_code.oracle.oracledb.connect")
def test_get_oracle_connection(mock_odb_connect, mock_odb_init_oracle_client, mock_env_access_key):
    """ test get orcale connection """
    mock_odb_init_oracle_client.return_value = True
    mock_odb_connect.return_value = True
    assert oracle.get_oracle_connection()
