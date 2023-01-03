""" Test for status/pts endpoint """
# pylint: disable=redefined-outer-name,unused-argument,unused-import
import json
from unittest.mock import patch
import azure.functions as func
from tests.fixtures import mock_env_access_key, mock_env_no_access_key, CLIENT_HEADERS
from status_pts import main

@patch("status_pts.get_oracle_connection")
@patch("status_pts.oracledb.clientversion")
def test_status_pts_function(mock_clientversion, mock_get_oracle_connection, mock_env_access_key):
    """ test_status_pts_function """

    mock_get_oracle_connection.return_value\
        .cursor.return_value.__enter__.return_value.execute.return_value\
                = [True]

    mock_clientversion.return_value\
            = 0
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='GET',
        body=None,
        headers=CLIENT_HEADERS,
        url='/api/status/pts')

    # Call the function.
    resp = main(req)
    # print response body
    print(resp.get_body())
    # loads response body as json
    resp_json = json.loads(resp.get_body())

    # Check the output.
    assert resp_json['status'] == 'success'


def test_status_pts_function_other(mock_env_access_key):
    """ test_status_pts_function_other """
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='POST',
        body="TEST",
        headers=CLIENT_HEADERS,
        url='/api/status/pts')

    # Call the function.
    resp = main(req)

    assert resp.status_code == 200

def test_status_pts_function_request_error(mock_env_no_access_key):
    """ test_status_pts_function_request error """

    with patch('status_http.func_json_response') as mock:
        mock.side_effect = ValueError('ERROR_TEST')
        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/status/pts')

        # Call the function.
        resp = main(req)

        resp_json = json.loads(resp.get_body())
        print(resp_json)
        # Check the output.
        assert resp_json['status'] == 'error'
