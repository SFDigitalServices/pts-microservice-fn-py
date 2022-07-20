""" permit_post init file """
import os
import json
import logging
import traceback
import requests
import jsend
import azure.functions as func
from requests.models import Response
from shared_code.common import func_json_response

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    main function for permit_post
    """
    logging.info('Permit POST processed a request.')

    try:
        response = Response()
        headers = {
            "Access-Control-Allow-Origin": "*"
        }
        if req.get_body() and len(req.get_body()):
            response.status_code = 200

            # pylint: disable=protected-access
            response._content = b'"200 Accepted POST"'
        else:
            response.status_code = 200

            # pylint: disable=protected-access
            response._content = b'"200 OK POST"'

        return func_json_response(response, headers, "message")

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("Status HTTP error occurred: %s", traceback.format_exc())

        msg_error = f"This endpoint encountered an error. {err}"
        func_response = json.dumps(jsend.error(msg_error))
        return func.HttpResponse(func_response, status_code=500)
