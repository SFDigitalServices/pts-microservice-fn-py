""" Test for permit_post endpoint """
# pylint: disable=redefined-outer-name,unused-argument,unused-import
import json
from unittest.mock import patch, Mock
import azure.functions as func
from tests.fixtures import mock_env_access_key, CLIENT_HEADERS, mock_cursor
from permit_post import main
import tests.mocks.permit_post_stored_proc_response as sp_mock

@patch("permit_post.get_oracle_connection")
def test_permit_post_function(mock_get_oracle_connection, mock_env_access_key):
    """ test_permit_post_function """

    # mock body
    with open('tests/mocks/permit_post_request.json', mode="rb") as file_handle:
        mock_body = file_handle.read()

    with open('tests/mocks/permit_post_response.json', encoding="UTF-8") as file_handle:
        mock_response = json.load(file_handle)
        mock_values =list(mock_response["data"]["out"].values())
        mock_side_effect = map(mock_cursor, mock_values)

    mock_get_oracle_connection.return_value\
        .cursor.return_value.__enter__.return_value.var.side_effect\
                = Mock(side_effect=mock_side_effect)

    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='POST',
        headers=CLIENT_HEADERS,
        body=mock_body,
        url='/api/permit')

    # Call the function.
    resp = main(req)
    # print response body
    print(resp.get_body())
    # loads response body as json
    resp_json = json.loads(resp.get_body())

    # Check the output.
    assert resp_json['status'] == 'success'

@patch("permit_post.get_oracle_connection")
def test_permit_post_function_address_not_found(mock_get_oracle_connection, mock_env_access_key):
    """ test_permit_post_function when stored proc returns address not found error """

    # mock body
    with open('tests/mocks/permit_post_request.json', mode="rb") as file_handle:
        mock_body = file_handle.read()

    mock_side_effect = map(mock_cursor, sp_mock.error_response.values())
    mock_get_oracle_connection.return_value\
        .cursor.return_value.__enter__.return_value.var.side_effect\
                = Mock(side_effect=mock_side_effect)

    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='POST',
        headers=CLIENT_HEADERS,
        body=mock_body,
        url='/api/permit')

    # Call the function.
    resp = main(req)
    # print response body
    print(resp.get_body())
    # loads response body as json
    resp_json = json.loads(resp.get_body())

    # Check the output.
    assert resp_json['status'] == 'error'

@patch("permit_post.get_oracle_connection")
def test_permit_post_oracle_error(mock_get_oracle_connection, mock_env_access_key):
    """ test permit_post when oracle throws an error """

    # mock body
    with open('tests/mocks/permit_post_request.json', mode="rb") as file_handle:
        mock_body = file_handle.read()

    mock_side_effect = map(mock_cursor, sp_mock.error_response.values())
    mock_get_oracle_connection.return_value\
        .cursor.return_value.__enter__.return_value.var.side_effect\
                = Mock(side_effect=mock_side_effect)
    mock_get_oracle_connection.return_value\
        .cursor.return_value.__enter__.return_value.callproc.side_effect\
                = Exception("oracle error")

    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='POST',
        headers=CLIENT_HEADERS,
        body=mock_body,
        url='/api/permit')

    # Call the function.
    resp = main(req)
    # print response body
    print(resp.get_body())
    # loads response body as json
    resp_json = json.loads(resp.get_body())

    # Check the output.
    assert resp_json['status'] == 'error'

def test_permit_post_function_other(mock_env_access_key):
    """ test_permit_post_function_other """
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='POST',
        headers=CLIENT_HEADERS,
        body=None,
        url='/api/permit')

    # Call the function.
    resp = main(req)

    assert resp.status_code == 200

def test_permit_post_function_request_error():
    """ test_permit_post_function_request_error error """

    with patch('permit_post.func_json_response') as mock:
        mock.side_effect = ValueError('ERROR_TEST')
        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method='POST',
            body=None,
            url='/api/permit')

        # Call the function.
        resp = main(req)

        resp_json = json.loads(resp.get_body())
        print(resp_json)
        # Check the output.
        assert resp_json['status'] == 'error'
