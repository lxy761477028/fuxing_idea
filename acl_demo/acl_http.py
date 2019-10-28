from flask import Flask
import json
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/', methods=['POST'])
def dispatch():
    input_json = request.json
    print(input_json)
    input_json.get("method")
    input_json.get("data")
    data = {
        "beginTime": 1566537461182,
        "code": 0,
        "data": {"2019-08-09-132950#1-1":
                     {"cell_ratio":0.5,
                      "sample_details":[{
                          "image_details":{"prob":0.9,"type":1},
                          "image_name":"image_1",
                          "image_result":1,
                          "sample_name":"2019-08-09-132950#1-1"},
                          {"image_details":{"prob":0.9,"type":1},
                           "image_name":"image_2",
                           "image_result":1,
                           "sample_name":"2019-08-09-132950#1-1"},
                          {"image_details":{"prob":0.9,"type":1},
                           "image_name":"image_3",
                           "image_result":1,
                           "sample_name":"2019-08-09-132950#1-1"}],
                      "sample_result":1,"task_type":1}},
        "endTime": 1566537461185,
        "requestId": 44
    }
    data = json.dumps(data)
    return data

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)