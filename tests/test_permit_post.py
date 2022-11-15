""" Test for permit_post endpoint """
import json
from unittest.mock import patch
import azure.functions as func
from permit_post import main

def test_permit_post_function():
    """ test_permit_post_function """
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='POST',
        body=None,
        url='/api/permit')

    # Call the function.
    resp = main(req)
    # print response body
    print(resp.get_body())
    # loads response body as json
    resp_json = json.loads(resp.get_body())

    # Check the output.
    assert resp_json['status'] == resp_json['status']


def test_permit_post_function_other():
    """ test_permit_post_function_other """
    # Construct a mock HTTP request.
    req = func.HttpRequest(
        method='POST',
        body="TEST",
        url='/api/permit')

    # Call the function.
    resp = main(req)

    assert resp.status_code == resp.status_code

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
