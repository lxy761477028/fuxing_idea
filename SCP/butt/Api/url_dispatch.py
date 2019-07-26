from flask import Blueprint
from flask import request
from flask import app
import requests
import json
import pymysql
from config import Config
from config import mysqlConfig
from config import tokenConfig
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature


algs_blu = Blueprint("algs", __name__)


@algs_blu.route('/')
def hello_world():
    # f = Config.REQUEST_ID
    # print(f)
    return 'Hello World! zenmhuishier'


@algs_blu.route('/', methods=['POST'])
def dispatch():
    input_json = request.json
    tenantCode = input_json.get("tenantCode")
    patientUid = input_json.get("patientUid")
    studyInstanceUID = input_json.get("studyInstanceUID")
    url = input_json.get("url")
    diagStatus = input_json.get("diagStatus")
    abnormal = input_json.get("abnormal")
    data = {
        "appId": Config.APPLD,
        "license": Config.LICENSE
    }
    data = {
        "token":"9351f5c11aff4030b200f9a359057eca"
        }
    response = requests.post(Config.URL + "demo/v1/auth/getToken", json=data)
    response_test = json.loads(response.text)
    print(response_test)

    token = response_test["result"][0]["token"]
    headers = {"token": token}
    data = {
        "studyInstanceUID": studyInstanceUID,
        "url": url,
        "abnormal": abnormal,
        "diagStatus": diagStatus
    }
    response = requests.post(Config.URL + "/v1/ai/pushAIDiagResult", headers=headers, json=data)

    db = pymysql.connect(host=MYSQLConfig.HOST, port=MYSQLConfig.PORT, user=MYSQLConfig.USER,
                         password=MYSQLConfig.PASSWORD, database=MYSQLConfig.DATABASE)
    cursor = db.cursor()
    try:
        cursor.execute('insert into t_study_ai_result values(null, %s, %s, %s, %s, %s, %s, now(), now())'
                       % (tenantCode, patientUid, studyInstanceUID, url, diagStatus, abnormal))
        db.commit()
    except:
        db.rollback()
    db.close()
    return 'Hello World!'


@algs_blu.route('/v1/auth/getToken', methods=['POST'])
def getToken():
    input_json = request.json
    appId = input_json.get("appId")
    license = input_json.get("license")
    try:
        if appId == tokenConfig.APPLD and license == tokenConfig.LICENSE:
            token = generate_auth_token(appId, license,expiration=20)
            data = {
                    "status": tokenConfig.SUCCESS,
                    "message": "成功",
                    "result": [{
                            "token": token
                        }]
                    }
        else:
            data = {
                    "status": tokenConfig.FAIL,
                    "message": "失败",
                    "result": []
                    }
    except Exception as e:
        data = {
                "status": tokenConfig.FAIL,
                "message": e,
                "result": []
                    }
    return data


@algs_blu.route('/v1/ai/pushRptDiagResult', methods=['POST'])
def pushRptDiagResult():
    s = TimedJSONWebSignatureSerializer("123456")
    token = request.headers["token"]
    try:
        data = s.loads(token, return_header=True)
        input_json = request.json
        studyInstanceUID = input_json.get("studyInstanceUID")
        description = input_json.get("description")
        impression = input_json.get("impression")
        abnormal = input_json.get("abnormal")

        db = pymysql.connect(host=MYSQLConfig.HOST, port=MYSQLConfig.PORT, user=MYSQLConfig.USER,
                             password=MYSQLConfig.PASSWORD, database=MYSQLConfig.DATABASE)
        cursor = db.cursor()
        try:
            cursor.execute('insert into t_study_pacs_info values(null, %s, %s, %s, %s, now())'
                           % (studyInstanceUID, description, impression, abnormal))
            db.commit()
        except:
            db.rollback()
        db.close()
        data = {
            "status" : 0,
            "message" : "success"
        }
    except Exception as e:
        data = {
            "status": 1,
            "message": e
        }
    return data


def generate_auth_token(appId, license, expiration=20):
    s = TimedJSONWebSignatureSerializer("123456",
                   expires_in=expiration)
    return s.dumps({
        'appId': appId,
        'license': license,

    }).decode('ascii')


@algs_blu.route('/v1/auth/mq_listen', methods=['POST'])
def mqListen():
    # input_json = request.json
    # tenantCode = input_json.get("tenantCode")
    # patientUid = input_json.get("patientUid")
    # studyInstanceUID = input_json.get("studyInstanceUID")
    # url = input_json.get("url")
    # diagStatus = input_json.get("diagStatus")
    # abnormal = input_json.get("abnormal")
    # data = {
    #     "appId": Config.APPLD,
    #     "license": Config.LICENSE
    # }
    # data = {
    #     "token":"9351f5c11aff4030b200f9a359057eca"
    #     }
    # response = requests.post(Config.URL + "demo/v1/auth/getToken", json=data)
    # response_test = json.loads(response.text)
    # print(response_test)
    #
    # token = response_test["result"][0]["token"]
    # headers = {"token": token}
    # data = {
    #     "studyInstanceUID": studyInstanceUID,
    #     "url": url,
    #     "abnormal": abnormal,
    #     "diagStatus": diagStatus
    # }
    # response = requests.post(Config.URL + "/v1/ai/pushAIDiagResult", headers=headers, json=data)
    #
    # db = pymysql.connect(host=MYSQLConfig.HOST, port=MYSQLConfig.PORT, user=MYSQLConfig.USER,
    #                      password=MYSQLConfig.PASSWORD, database=MYSQLConfig.DATABASE)
    # cursor = db.cursor()
    # try:
    #     cursor.execute('insert into t_study_ai_result values(null, %s, %s, %s, %s, %s, %s, now(), now())'
    #                    % (tenantCode, patientUid, studyInstanceUID, url, diagStatus, abnormal))
    #     db.commit()
    # except:
    #     db.rollback()
    # db.close()
    return 'hello word'