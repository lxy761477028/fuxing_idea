from flask import Flask
import time
import requests
import random
import json
from flask import request


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/', methods=['POST'])
def dispatch():
    json_data = request.json
    print(json_data)
    lt = ["1804533", "9354384", "20198416", "1804504"]
    radnnum = random.randint(0,3)
    st1 = lt[radnnum]
    data = {
        "code": 0,
        "data":{
            "ocr_res": st1,
        }
    }
    json_data = json.dumps(data)
    return json_data


@app.route('/ring-server/v1/recognition/statistics', methods=['POST'])
def statistics():
    json_data = request.json
    url_data = request.url
    print(json_data)
    print(url_data)
    lt = ["1804533", "9354384", "20198416", "1804504"]
    radnnum = random.randint(0,3)
    st1 = lt[radnnum]
    data = {
    "code": 0,
    "data": {
        "is_recognition": False,
        "imagePath": "/data/ring/deploy/static/bridge/20191206/output_add5b8822d8645f98759d15a853fdebc.png"
    }}
    json_data = json.dumps(data)
    return json_data


if __name__ == '__main__':
    app.run(port=6000)
