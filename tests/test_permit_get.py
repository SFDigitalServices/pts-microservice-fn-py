""" Test for status/http endpoint """
# pylint: disable=redefined-outer-name,unused-argument,unused-import
import json
from unittest.mock import patch, Mock
import azure.functions as func
from tests.fixtures import mock_env_access_key, mock_env_no_access_key, CLIENT_HEADERS, mock_cursor
from permit_get import main

@patch("permit_get.get_oracle_connection")
def test_permit_get_function(mock_get_oracle_connection, mock_env_access_key):
    """ test_permit_get_function """

    with open('tests/mocks/permit_get_by_address_request.json', mode="rb") as file_handle:
        mock_params = json.load(file_handle)

    with open('tests/mocks/permit_get_response.json', encoding="UTF-8") as file_handle:
        mock_oracle_response = json.load(file_handle)

    mock_get_oracle_connection.return_value\
        .cursor.return_value.__enter__.return_value.callfunc.return_value\
                = mock_oracle_response

    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='GET',
        headers=CLIENT_HEADERS,
        body=None,
        url='/api/permit',
        params=mock_params)

    # Call the function.
    resp = main(req)

    # print response body
    print(resp.get_body())

    # loads response body as json
    resp_json = json.loads(resp.get_body())

    # Check the output.
    assert resp_json['status'] == 'success'

def test_permit_get_function_request_error(mock_env_no_access_key):
    """ test_permit_get_function error """

    with patch('permit_get.func_json_response') as mock:
        mock.side_effect = ValueError('ERROR_TEST')
        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/permit')

        # Call the function.
        resp = main(req)

        resp_json = json.loads(resp.get_body())
        print(resp_json)

        # Check the output.
        assert resp_json['status'] == 'error'
