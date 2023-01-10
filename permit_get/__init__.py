""" permit_get init file """
import os
import json
import logging
import traceback
import requests
import jsend
import oracledb

import azure.functions as func
from requests.models import Response
from shared_code.common import func_json_response, validate_access, get_http_response_by_status
from shared_code.oracle import get_oracle_connection

#pylint: disable=unused-argument, too-many-locals
def main(req: func.HttpRequest) -> func.HttpResponse:
    """ main function for permit_get """
    logging.info('Permit GET processed a request.')

    try:
        response = Response()
        json_root = "message"
        out = None
        headers = {
            "Access-Control-Allow-Origin": "*"
        }

        if req.params.get('avs_address_id'):
            response.status_code = 200
            sp_param = [
                "P_AVS_ADDRESS_ID"
            ]

            connection = get_oracle_connection()
            with connection.cursor() as cursor:
                data_json =  {}
                data_json["P_AVS_ADDRESS_ID"] = req.params.get('avs_address_id')

                params = []
                for field in sp_param:
                    value = data_json[field] if field in data_json else ''
                    params.append(value)

                values = cursor.callfunc("pts.sp_rpt_get_filed_permits", oracledb.CURSOR, params)

                existing_permits = []
                keys = [
                    "application_number",
                    "description",
                    "current_status",
                    "currrent_date",
                    "APPLICATION_CREATION_DATE",
                    "Applicant_name",
                    "role"]
                for value in values:
                    permit = {}
                    for idx, key in enumerate(keys):
                        permit[key.upper()] = str(value[idx])
                    existing_permits.append(permit)

                json_root = "out"
                out = {"P_PERMITS": existing_permits}

            print(out)
        else:
            response.status_code = 200

            out = "200 OK GET"

        return func_json_response(response, headers, json_root, out)

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("Status HTTP error occurred: %s", traceback.format_exc())
        msg_error = f"This endpoint encountered an error. {err}"
        func_response = json.dumps(jsend.error(msg_error))
        return func.HttpResponse(func_response, status_code=500)
