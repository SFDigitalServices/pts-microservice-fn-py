""" Test for status/http endpoint """
# pylint: disable=redefined-outer-name,unused-argument,unused-import
import json
from unittest.mock import patch
import azure.functions as func
from tests.fixtures import mock_env_access_key, mock_env_no_access_key, CLIENT_HEADERS
from permit_get import main


def test_permit_get_function(mock_env_access_key):
    """ test_permit_get_function """
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='GET',
        headers=CLIENT_HEADERS,
        body=None,
        url='/api/permit')

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
