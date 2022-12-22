""" permit_post init file """
import os
import json
import logging
import traceback
import requests
import jsend
import azure.functions as func
from requests.models import Response
from shared_code.common import func_json_response, validate_access
from shared_code.oracle import get_oracle_connection
from shared_code.pts import get_pts_out

#pylint: disable=too-many-locals
def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    main function for permit_post
    """
    logging.info('Permit POST processed a request.')

    try:
        validate_access(req)
        response = Response()
        out = None
        json_root = "message"
        headers = {
            "Access-Control-Allow-Origin": "*"
        }

        if req.get_body() and req.get_json() and len(req.get_json()):
            response.status_code = 200
            req_json = req.get_json()

            # initialize out. with EXT_{fields} fields if any
            out = {key: val for key, val in req_json.items() if key.startswith('EXT_')}

            sp_gen_permit = [
                "P_AVS_ADDRESS_ID",
                "P_SCOPE_OF_WORK",
                "P_COMPLAINT_NUMBER",
                "P_AFFORDABLE_HOUSING",
                "P_NEW_CONST",
                "P_REVISION",
                "P_RELATED_APP_NUM",
                "P_VALUATION",
                "P_APPLICANT_FIRST_NAME",
                "P_APPLICANT_LASTINNAME",
                "P_APPLICANT_EMAIL_ADDRESS",
                "P_APPLICANT_PHONE_NUMBER",
                "P_APPLICANT_LICENSE_NUMBER",
                "P_APPLICANT_ROLE",
                "P_CONTACT1_FIRST_NAME",
                "P_CONTACT1_LASTINNAME",
                "P_CONTACT1_EMAIL_ADDRESS",
                "P_CONTACT1_PHONE_NUMBER",
                "P_CONTACT1_LICENSE_NUMBER",
                "P_CONTACT1_ROLE",
                "P_CONTACT2_FIRST_NAME",
                "P_CONTACT2_LASTINNAME",
                "P_CONTACT2_EMAIL_ADDRESS",
                "P_CONTACT2_PHONE_NUMBER",
                "P_CONTACT2_LICENSE_NUMBER",
                "P_CONTACT2_ROLE",
                "P_STATUS",
                "P_MSG",
                "P_APP_NUM",
                "P_FORMIO"
            ]

            connection = get_oracle_connection()
            with connection.cursor() as cursor:
                data_json =  req_json
                data_json["P_STATUS"] = cursor.var(str)
                data_json["P_MSG"] = cursor.var(str)
                data_json["P_APP_NUM"] = cursor.var(str)

                params = []
                for field in sp_gen_permit:
                    value = data_json[field] if field in data_json else ''
                    params.append(value)
                #bool_result = cursor.callfunc("pts.sp_gen_permit", int, params)
                #print(bool_result)
                cursor.callproc("pts.sp_gen_permit", params)
                print("p_status: " + str(data_json["P_STATUS"].getvalue()))
                print("p_msg: " + str(data_json["P_MSG"].getvalue()))
                print("p_app_num: " + str(data_json["P_APP_NUM"].getvalue()))

                if data_json["P_APP_NUM"].getvalue():
                    response.status_code = 200
                    json_root = "out"
                    out = get_pts_out(data_json, out)
                    out["P_APP_NUM"] = data_json["P_APP_NUM"].getvalue()

            print(out)
        else:
            response.status_code = 200

            # pylint: disable=protected-access
            response._content = b'"200 OK POST"'

        return func_json_response(response, headers, json_root, out)

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("Status HTTP error occurred: %s", traceback.format_exc())

        msg_error = f"This endpoint encountered an error. {err}"
        func_response = json.dumps(jsend.error(msg_error))
        return func.HttpResponse(func_response, status_code=500)
