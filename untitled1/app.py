from flask import Flask
import time
import random
from flask import request


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/', methods=['POST'])
def dispatch():
    json_data = request.json
    num = random.randint(0, 15)
    time.sleep(num)

    return json_data


if __name__ == '__main__':
    app.run(port=6000)
