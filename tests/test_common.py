""" Test for common functions """
# pylint: disable=redefined-outer-name,unused-argument,unused-import
from tests.fixtures import mock_env_access_key
from shared_code import common

def test_get_http_response_by_status(mock_env_access_key):
    """ test get get_http_response_by_status function """
    resp = common.get_http_response_by_status(200)
    assert resp.content.decode() == '"200 OK"'

    resp = common.get_http_response_by_status(500)
    assert resp.content.decode() == '"500 Internal Server Error"'
