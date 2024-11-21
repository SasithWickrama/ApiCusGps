import random
import traceback
import calendar
import time
import datetime
from flask import Flask, request
from flask_restful import Api, Resource
import db

app = Flask(__name__)
api = Api(app)

def random_ref(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    return ''.join((random.choice(sample_string)) for x in range(length))

class CustomerData(Resource):

    @staticmethod
    def execute_db(data):
        conn = db.DbConnection.dbconnClarity()
        result = {}

        try:
            required_keys = ['NIC', 'OID', 'RTOM', 'UID', 'LON', 'LAT', 'DP', 'ATT']
            if not all(key in data for key in required_keys):
                result['msg'] = "Required parameter cannot be null"
                return result

            cursor = conn.cursor()

            sql = 'SELECT COUNT(*) FROM OSSRPT.GPS_CUS_LOC_180 WHERE CRM_REF_ID = :CRM_REF_ID'
            cursor.execute(sql, {'CRM_REF_ID': data['OID']})
            nrec = cursor.fetchone()[0]

            if nrec == 0:
                current_GMT = time.gmtime()
                time_stamp = calendar.timegm(current_GMT)
                today = datetime.date.today()
                year = today.strftime('%y')
                month = today.strftime('%m')
                day = today.strftime('%d')
                eqid = 'FM' + year + month + day + str(time_stamp)

                sql2 = "INSERT INTO GPS_CUS_LOC_180 (CUS_REF_ID, CRM_REF_ID, LON, LAT, RTOM, DP, CREATE_DATE, EQ_TYPE) VALUES (:CUS_REF_ID, :CRM_REF_ID, :LON, :LAT, :RTOM, :DP, SYSDATE, 'CUS')"
                cursor.execute(sql2, {'CUS_REF_ID': eqid, 'CRM_REF_ID': data['OID'], 'LON': data['LON'], 'LAT': data['LAT'], 'RTOM': data['RTOM'], 'DP': data['DP']})
                conn.commit()

                sql3 = "SELECT * FROM OSSRPT.GPS_CUS_LOC_ATT_LIST"
                cursor.execute(sql3)

                for row2 in cursor.fetchall():  # Use fetchall() instead of iterating directly over cursor
                    att_name = row2[0]  # Assuming the first column is ATT_NAME
                    if att_name in ['CUSTOMER NAME', 'NIC', 'USER ID', 'PAYMENT', 'MOBILE NO', 'REMARKS']:
                        att_value = data['ATT'][0] if att_name == 'PAYMENT' else data['ATT'][1] if att_name == 'CUSTOMER NAME' else data[att_name]
                        sql4 = "INSERT INTO GPS_CUS_LOC_ATT_180 (CUS_REF_ID, ATT_NAME, ATT_VALUE, ATT_ID) VALUES (:CUS_REF_ID, :ATT_NAME, :ATT_VALUE, GPS_CUS_180_ATTSEQ.nextval)"
                        cursor.execute(sql4, {'CUS_REF_ID': eqid, 'ATT_NAME': att_name, 'ATT_VALUE': att_value})
                        conn.commit()

                result['msg'] = "Success"
                result['data'] = eqid

            else:
                result['msg'] = "Data Already Exist"

        except Exception as e:
            print(e)
            result['msg'] = str(e)

        finally:
            if 'cursor' in locals():
                cursor.close()
            conn.close()

        return result

class AddCustomerData(Resource):
    @staticmethod
    def post():
        data = request.get_json()
        if not data:
            return {"msg": "No data provided"}, 400
        ref = random_ref(15)
        return CustomerData.execute_db(data)

api.add_resource(AddCustomerData, '/ApiCusGps/addcusData/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=22750)
