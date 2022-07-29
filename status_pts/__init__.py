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
from shared_code.common import func_json_response

def main(req: func.HttpRequest) -> func.HttpResponse:
    """ main function for status/pts """
    logging.info('Status PTS processed a request.')

    try:
        headers = {
            "Access-Control-Allow-Origin": "*"
        }
        response = Response()
        out = None
        if req.get_body() and len(req.get_body()):
            response = requests.get('https://ifconfig.me')
            out = str(response.text)
        else:
            usr = os.environ.get('PTS_USERNAME')
            pwd = os.environ.get('PTS_PASSWORD')
            cns = os.environ.get('PTS_CONNECTSTRING')

            lib_dir = os.environ.get('ORACLE_LIB_DIR')
            print(lib_dir)
            oracledb.init_oracle_client(lib_dir)
            with oracledb.connect(user=usr, password=pwd, dsn=cns) as connection:
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
