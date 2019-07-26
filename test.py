from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from flask import Flask
import time

app = Flask(__name__)

@app.route('/',methods=['GET'])
def sayHello():
    time.sleep(10)
    return 'hello'

@app.route('/hi',methods=['GET'])
def sayHi():
    return 'hi'
if __name__ =='__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()