import json
import random
from datetime import timedelta
import traceback
import requests
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
#from log import Logger
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import calendar
import time
import datetime
import db

 

app = Flask(__name__)

#app.config['PROPAGATE_EXCEPTIONS'] = True
#app.config["JWT_SECRET_KEY"] = const.JWT_SECRET_KEY
#app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
#jwt = JWTManager(app)
api = Api(app)

#logger = Logger.getLogger('server_requests', 'logs/server_requests')

#loggerMob = Logger.getLogger('MobitelLtefaults', 'logs/MobitelLtefaults')


def random_ref(length):

    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    # define the condition for random string
    return ''.join((random.choice(sample_string)) for x in range(length))

'''
@jwt.expired_token_loader

def my_expired_token_callback(jwt_header, jwt_data):

    return jsonify({"result": "error", "msg": "Token has expired"}), 401


@jwt.invalid_token_loader

def my_invalid_token_callback(jwt_data):

    return jsonify({"result": "error", "msg": "Invalid Token"}), 401


@jwt.unauthorized_loader

def my_unauthorized_loader_callback(jwt_data):

    return jsonify({"result": "error", "msg": "Missing Authorization Header"}), 401

 
def getAuthKey(userid):

    with open('auth.json') as f:

        data = json.load(f)

        for usr in data['user_list']:

            if usr['username'] == str(userid):

                return usr['authkey']

 

# TOKEN

class GetToken(Resource):

    def get(self):

        ref = random_ref(15)

        logger.info(ref + " - " + str(request.remote_addr) + " - " + str(request.url) + " - " + str(request.headers))

        data = request.get_json()

        return Authenticate.generateToken(data, ref)

headers = {

    'Content-type': 'application/json',

    'Accept': 'application/json'}

auth = HTTPBasicAuth('SLTUSR', 'SLTPW') 
'''


class addCustomerData(Resource):

    @staticmethod
    def exeDb(data, ref):
        conn = db.DbConnection.dbconnClarity("")
        result = {}  # Initialize result here

        try:
            if data['NIC'] and data['OID'] and data['RTOM'] and data['UID'] and data['LON'] and data['LAT'] and data['DP']:
                sql = 'SELECT COUNT(*) FROM OSSRPT.GPS_CUS_LOC_180 WHERE CRM_REF_ID = :CRM_REF_ID'
                c = conn['status'].cursor()
                c.execute(sql, {'CRM_REF_ID': data['OID']})
                data = []

                for row in c:
                    nrec = row[0]
                    if nrec == 0:
                        current_GMT = time.gmtime()
                        time_stamp = calendar.timegm(current_GMT)
                        today = datetime.date.today()
                        year = today.strftime('%y')
                        month = today.month
                        day = today.day
                        eqid = 'FM'+year + '' + month + '' + day + '' + time_stamp

                        sql2 = "INSERT INTO GPS_CUS_LOC_180 (CUS_REF_ID, CRM_REF_ID, LON, LAT, RTOM, DP, CREATE_DATE, EQ_TYPE) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}', SYSDATE,'CUS')".format(
                            eqid, data['OID'], data['LON'], data['LAT'], data['RTOM'], data['DP'])
                        c.execute(sql2)
                        c.execute("commit")

                        sql3 = "SELECT * FROM OSSRPT.GPS_CUS_LOC_ATT_LIST"
                        c.execute(sql3)

                        for row2 in c:
                            
                            if row2['ATT_NAME'] == 'CUSTOMER NAME':
                                sql4 = "INSERT INTO GPS_CUS_LOC_ATT_180 (CUS_REF_ID, ATT_NAME, ATT_VALUE, ATT_ID) VALUES ('{0}','{1}','{2}',GPS_CUS_180_ATTSEQ.nextval)".format(
                                    eqid, row2['ATT_NAME'], data['ATT'][1])
                                c.execute(sql4)
                                c.execute("commit")
                                
                            if row2['ATT_NAME'] == 'NIC':
                                sql4 = "INSERT INTO GPS_CUS_LOC_ATT_180 (CUS_REF_ID, ATT_NAME, ATT_VALUE, ATT_ID) VALUES ('{0}','{1}','{2}',GPS_CUS_180_ATTSEQ.nextval)".format(
                                    eqid, row2['ATT_NAME'], data['NIC'])
                                c.execute(sql4)
                                c.execute("commit")

                            if row2['ATT_NAME'] == 'USER ID':
                                sql4 = "INSERT INTO GPS_CUS_LOC_ATT_180 (CUS_REF_ID, ATT_NAME, ATT_VALUE, ATT_ID) VALUES ('{0}','{1}','{2}',GPS_CUS_180_ATTSEQ.nextval)".format(
                                    eqid, row2['ATT_NAME'], data['UID'])
                                c.execute(sql4)
                                c.execute("commit")
                                
                            if row2['ATT_NAME'] == 'PAYMENT':
                                sql4 = "INSERT INTO GPS_CUS_LOC_ATT_180 (CUS_REF_ID, ATT_NAME, ATT_VALUE, ATT_ID) VALUES ('{0}','{1}','{2}',GPS_CUS_180_ATTSEQ.nextval)".format(
                                    eqid, row2['ATT_NAME'], data['ATT'][0])
                                c.execute(sql4)
                                c.execute("commit")
                                
                            if row2['ATT_NAME'] == 'MOBILE NO':
                                sql4 = "INSERT INTO GPS_CUS_LOC_ATT_180 (CUS_REF_ID, ATT_NAME, ATT_VALUE, ATT_ID) VALUES ('{0}','{1}','{2}',GPS_CUS_180_ATTSEQ.nextval)".format(
                                    eqid, row2['ATT_NAME'], data['ATT'][2])
                                c.execute(sql4)
                                c.execute("commit")
                                
                            if row2['ATT_NAME'] == 'REMARKS':
                                sql4 = "INSERT INTO GPS_CUS_LOC_ATT_180 (CUS_REF_ID, ATT_NAME, ATT_VALUE, ATT_ID) VALUES ('{0}','{1}','{2}',GPS_CUS_180_ATTSEQ.nextval)".format(
                                    eqid, row2['ATT_NAME'], data['ATT'][3])
                                c.execute(sql4)
                                c.execute("commit")
                                
                        #result['msg'] = "Success"
                        #result['data'] = eqid
                        return {"msg" : "Success", "data"  : str(eqid)}

                        #return result

                    else:
                        result['msg'] = "Data Already Exist"
                        return result

            else:
                result['msg'] = "Required parameter cannot be null"
                return result

        except Exception as e:
            print(e)
            result['msg'] = str(e)
            return result


# AddCustomerData
class addcusData(Resource):

    @staticmethod
    def post():
        ref = random_ref(15)
        data = request.get_json()
        return addCustomerData.exeDb(data, ref)



# API URL PATH
api.add_resource(addcusData, '/ApiCusGps/addcusData/')

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=22550)

    #serve(app, host='0.0.0.0', port=20001, threads=3)
