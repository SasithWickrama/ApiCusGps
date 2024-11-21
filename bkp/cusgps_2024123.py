import json

import random

from datetime import timedelta

import traceback

import requests

from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from pcrf.pcrf import Pcrf

from log import Logger

from flask import Flask, request, jsonify

from flask_restful import Api, Resource

#from waitress import serve

 

#from auth import Authenticate

#from sms.sendSms import Sendsms

#from lte.lteProv import Lteprov

#from ytul.ytulProv import Ytulprov

#from requests.auth import HTTPBasicAuth

#import const

import db

 

from csfeatureupd.csfeatureupd import CSfeatureupd

from entportal.getfaultdetails import Getfaultdetails

 

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

app.config["JWT_SECRET_KEY"] = const.JWT_SECRET_KEY

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)

jwt = JWTManager(app)

api = Api(app)

#logger = Logger.getLogger('server_requests', 'logs/server_requests')

#loggerMob = Logger.getLogger('MobitelLtefaults', 'logs/MobitelLtefaults')

def random_ref(length):

    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string

    # define the condition for random string

    return ''.join((random.choice(sample_string)) for x in range(length))


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

class addCustomerData(Resource):

    def post(self):

        conn = db.DbConnection.dbconnClarity("")

        data = request.get_json()

        try:

            if data ['NIC'] and data ['OID'] and data ['RTOM'] and data ['UID']:

                sql = 'SELECT COUNT(*) FROM OSSRPT.GPS_CUS_LOC_180 WHERE CRM_REF_ID = :CRM_REF_ID'

                c = conn['status'].cursor()

                c.execute(sql,{'CRM_REF_ID':data['OID']})

                result = {}

                data=[]

                nrec = row[0]

                if nrec == 0:

                    result['data'] = "Success"

                    return result

                else:

                    result['data'] = "Data Already Exsist"

                    return result

            else:

                result['data'] = "Required parameter can not be null"

                return result


        except Exception as e:

            print(e)

            result['data'] = e

            return result

# AddCustomerData
class addcusData(Resource):

    #@jwt_required()

    def post(self):

        ref = random_ref(15)

        data = request.get_json()

        return  addCustomerData.exeDb(data,ref)

# API URL PATH
api.add_resource(addcusData, '/api/storage/addcusData/')

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=22550)

    #serve(app, host='0.0.0.0', port=20001, threads=3)

    #Sasith