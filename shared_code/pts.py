""" Common PTS functions """

def get_pts_out(data_json):
    """ get standard PTS output from JSON """
    out = {
            "P_STATUS": data_json["P_STATUS"].getvalue(),
            "P_MSG": data_json["P_MSG"].getvalue()
            }
    return out
