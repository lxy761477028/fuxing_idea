from flask import Blueprint
from flask import request
# from config import Config


algs_blu = Blueprint("algs", __name__)


@algs_blu.route('/')
def hello_world():
    # f = Config.REQUEST_ID
    # print(f)
    return 'Hello World!'


@algs_blu.route('/', methods=['POST'])
def dispatch():
    input_json = request.json
    request_id = input_json.get()
    method = input_json.get()
    return 'Hello World!'
