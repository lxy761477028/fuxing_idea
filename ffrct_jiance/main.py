from flask import Flask
import requests
import os
import json

app = Flask(__name__)

@app.route('/ ', methods=['POST'])
def hello_world():
    host = "http://127.0.0.1:5010"
    data = {
          "method": "del_all_object",
          "ver": "2.0",
          "requestId": 44,
          "data":
          {
            "ser_id": "1.3.2.1258.55555455468.16",
          }
        }
    data = json.dumps(data)
    try:
        response = requests.post(host, json=data, timeout=3)
        data = {
                "beginTime": 0,
                "code": 0,
                "data": response,
                "endTime": 0,
                "requestId": 44
            }
    except:
        os.system("docker-compose -f /data/wangyaqi/docker_fix/ffrct_3.5.1.1/bin/all.yml down")
        os.system("docker-compose -f /data/wangyaqi/docker_fix/ffrct_3.5.1.1/bin/all.yml up -d")
        data = {
            "beginTime": 0,
            "code": 1,
            "data": "The service has been restarted.",
            "endTime": 0,
            "requestId": 44
        }

    data = json.dumps(data)
    return data





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)