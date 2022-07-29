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
from shared_code.oracle import get_oracle_connection

#pylint: disable=too-many-locals
def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    main function for permit_post
    """
    logging.info('Permit POST processed a request.')

    try:
        response = Response()
        out = None
        headers = {
            "Access-Control-Allow-Origin": "*"
        }

        if req.get_json() and len(req.get_json()):
            response.status_code = 200
            req_json = req.get_json()

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
                "P_CONTACT2_ROLE"
            ]
            params = []
            for field in sp_gen_permit:
                value = req_json[field] if field in req_json else ''
                params.append(value)

            connection = get_oracle_connection()
            with connection.cursor() as cursor:
                p_status = cursor.var(str)
                p_msg = cursor.var(str)
                p_app_num = cursor.var(str)
                params.append(p_status)
                params.append(p_msg)
                params.append(p_app_num)
                #bool_result = cursor.callfunc("pts.sp_gen_permit", int, params)
                #print(bool_result)
                cursor.callproc("pts.sp_gen_permit", params)
                print(p_status.getvalue())
                print(p_msg.getvalue())
                print(p_app_num.getvalue())

                if p_app_num.getvalue():
                    response.status_code = 200
                    out = p_app_num.getvalue()

            print(out)
        else:
            response.status_code = 200

            # pylint: disable=protected-access
            response._content = b'"200 OK POST"'

        return func_json_response(response, headers, "message", out)

    #pylint: disable=broad-except
    except Exception as err:
        logging.error("Status HTTP error occurred: %s", traceback.format_exc())

        msg_error = f"This endpoint encountered an error. {err}"
        func_response = json.dumps(jsend.error(msg_error))
        return func.HttpResponse(func_response, status_code=500)
