from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from flask import Flask
import os
from alg.url_dispatch import algs_blu
from config import Config
import logging

app = Flask(__name__)

log_dir = Config.LOGGING_FILE_PATH
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(filename="./log/log.txt", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


app.register_blueprint(blueprint=algs_blu)


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()