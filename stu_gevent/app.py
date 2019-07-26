from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from flask import Flask
import os
from alg.url_dispatch import algs_blu
from config import Config
import logging.config
# from logging_config import Logger


app = Flask(__name__)

log_dir = Config.LOGGING_FILE_PATH
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# log = Logger('./log/all.log',level='debug')
# log.logger.debug('debug')
# # file_handler = logging.FileHandler("./log/log.txt")
# console_handler = logging.StreamHandler()
# # file_handler.setLevel('DEBUG')
# console_handler.setLevel('DEBUG')
#
# fmt = '%(asctime)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s'
# formatter = logging.Formatter(fmt)
# # file_handler.setFormatter(formatter)
# console_handler.setFormatter(formatter)
#
# logger = logging.getLogger(__name__)
# logger.setLevel('DEBUG')
#
# # logger.addHandler(file_handler)
# logger.addHandler(console_handler)
# #
logging.basicConfig(filename="./log/log.txt", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


app.register_blueprint(blueprint=algs_blu)


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()