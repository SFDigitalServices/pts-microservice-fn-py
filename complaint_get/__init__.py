""" permit_bb init file """
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
from shared_code.pts import get_pts_out

#pylint: disable=too-many-locals
def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    main function for complaint_get
    """
    logging.info('Complaint GET processed a request.')

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
                "P_AVS_ADDRESS_ID",
                "P_STATUS",
                "P_MSG"
            ]

            connection = get_oracle_connection()
            with connection.cursor() as cursor:
                data_json =  {}
                data_json["P_AVS_ADDRESS_ID"] = req.params.get('avs_address_id')
                data_json["P_STATUS"] = cursor.var(str)
                data_json["P_MSG"] = cursor.var(str)

                params = []
                for field in sp_param:
                    value = data_json[field] if field in data_json else ''
                    params.append(value)

                cursor.callproc("pts.sp_rpt_find_active_complaint", params)
                print("p_status: " + str(data_json["P_STATUS"].getvalue()))
                print("p_msg: " + str(data_json["P_MSG"].getvalue()))

                if data_json["P_STATUS"].getvalue():
                    json_root = "out"
                    out = get_pts_out(data_json)

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
