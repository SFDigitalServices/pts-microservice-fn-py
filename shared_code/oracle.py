""" oracle common helper functions """
import os
import oracledb

def get_oracle_connection():
    """ Get Oracle connection """
    usr = os.environ.get('PTS_USERNAME')
    pwd = os.environ.get('PTS_PASSWORD')
    cns = os.environ.get('PTS_CONNECTSTRING')

    lib_dir = os.environ.get('ORACLE_LIB_DIR')
    print(lib_dir)
    oracledb.init_oracle_client(lib_dir)
    return oracledb.connect(user=usr, password=pwd, dsn=cns)
