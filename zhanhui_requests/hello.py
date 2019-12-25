
import requests



def get_token():
    data = {
      "method": "read_dicom",
      "ver": "2.0",
      "requestId": 44,
      "data":
      {
        "ser_id": "1.3.2.1258.55555455468.16",
        "dicomPath" : "/opt/alpha/appdata/autotest/UT/FFRct_Adapters_UT/Data/1007855311/"
        }
    }
    response = requests.post("172.16.100.9:8088", json=data)

    print(response.text)