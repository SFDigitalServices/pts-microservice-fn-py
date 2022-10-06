""" status/pts init file """
import os
import json
import logging
import traceback
import requests
import jsend
import oracledb
import azure.functions as func
from requests.models import Response
from shared_code.common import func_json_response, validate_access
from shared_code.oracle import get_oracle_connection

def main(req: func.HttpRequest) -> func.HttpResponse:
    """ main function for status/pts """
    logging.info('Status PTS processed a request.')

    try:
        validate_access(req)
        headers = {
            "Access-Control-Allow-Origin": "*"
        }
        response = Response()
        out = None
        if req.get_body() and len(req.get_body()):
            response = requests.get('https://ifconfig.me')
            out = str(response.text)
        else:
            connection = get_oracle_connection()
            with connection.cursor() as cursor:
                print(oracledb.clientversion())
                sql = """select sysdate from dual"""
                for rtn in cursor.execute(sql):
                    print(rtn)
                    if rtn:
                        response.status_code = 200
                        out = "200 OK"

        return func_json_response(response, headers, "message", out)

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("Status HTTP error occurred: %s", traceback.format_exc())
        msg_error = f"This endpoint encountered an error. {err}"
        func_response = json.dumps(jsend.error(msg_error))
        return func.HttpResponse(func_response, status_code=500)
