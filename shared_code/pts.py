""" Common PTS functions """

def get_pts_out(data_json, out=None):
    """ get standard PTS output from JSON """
    out = out if out else {}
    pts_out = {
        "P_STATUS": data_json["P_STATUS"].getvalue(),
        "P_MSG": data_json["P_MSG"].getvalue()
        }
    out.update(pts_out)
    return out
