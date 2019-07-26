import telnetlib
import requests
# host = "127.0.0.1"
# port = 6000
#
# tn = telnetlib.Telnet(host, port)

input_json = {"mnk": "hkn"}
try:
    response = requests.post("http://127.0.0.0:6000", json=input_json)
except:
    print("失败")
    try:
        response = requests.post("http://127.0.0.0:6000", json=input_json)
    except:
        print("失败2")
        response = requests.post("http://127.0.0.1:6000", json=input_json)


print(response.text)