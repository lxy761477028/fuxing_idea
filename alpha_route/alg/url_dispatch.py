import time
# from app import algs_blu
from flask import Blueprint
from flask import request
import requests
import telnetlib
import logging
# from logging_config import Logger


from config import Config


algs_blu = Blueprint("algs", __name__)


tring = 0
obj_dict ={}
obj_dict["AII_POST"] = 0
for i in range(len(Config.AI_SERVING)):
    obj_dict[Config.AI_SERVING[i][0]] = 0
tel_dict ={}
for i in range(len(Config.AI_SERVING)):
    tel_dict[Config.AI_SERVING[i][0]] = True


log = logging.getLogger(__name__)


# log.logger.debug('debug')

@algs_blu.route('/', methods=['POST'])
def sayHello():
    input_json = request.json
    log.warning('ApiInput : [%s]', input_json)

    # log.logger.debug('ApiInput : [%s]', input_json)
    result = dispatch_alg(input_json)

    return result


@algs_blu.route('/hi', methods=['GET'])
def sayHi():
    return 'hi'


def dispatch_alg(input_json):
    # response = requests.post(Config.AI_URL+":" + str(Config.AI_PORT[0]), json=input_json)
    # json_data = response.text
    for i in range(len(Config.AI_SERVING)):
        host = Config.AI_SERVING[i][1]
        port = Config.AI_SERVING[i][2]
        try:
            tn = telnetlib.Telnet(host, port)
            tel_dict[Config.AI_SERVING[i][0]] = True
        except Exception as e:
            tel_dict[Config.AI_SERVING[i][0]] = False


    ALL_PROCESSES = 0
    for i in range(len(Config.AI_SERVING)):
        if tel_dict[Config.AI_SERVING[i][0]]:
            ALL_PROCESSES += Config.AI_SERVING[i][3]

    if obj_dict["AII_POST"] <= ALL_PROCESSES:
        obj_dict["AII_POST"] += 1
        port_sign = get_port()
        obj_dict[Config.AI_SERVING[port_sign][0]] += 1
        try:
            response = requests.post("http://" + Config.AI_SERVING[port_sign][1] + ":" + str(Config.AI_SERVING[port_sign][2]), json=input_json)
            data = response.text
        except Exception as e:
            try:
                if len(Config.AI_SERVING) >= 2:
                    tel_dict[Config.AI_SERVING[port_sign][0]] = False
                    port_sign = get_port()
                    response = requests.post("http://" + Config.AI_SERVING[port_sign][1] + ":" + str(Config.AI_SERVING[port_sign][2]),json=input_json)
            except:
                print("shiabi")
        obj_dict[Config.AI_SERVING[port_sign][0]] -= 1
        obj_dict["AII_POST"] -= 1
    else:
        return "ai is busy"
    return str(Config.AI_SERVING[port_sign])


def get_port():
    port_num = 1
    port_sign = 0
    for i in range(len(Config.AI_SERVING)):
        if tel_dict[Config.AI_SERVING[i][0]]:
            usage_rate = obj_dict[Config.AI_SERVING[i][0]]/Config.AI_SERVING[i][3]
            if usage_rate <= port_num:
                port_num = usage_rate
                port_sign = i
    return port_sign



