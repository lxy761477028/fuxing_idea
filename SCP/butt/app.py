from flask import Flask
from gevent import monkey

from Api.url_dispatch import algs_blu



monkey.patch_all()
app = Flask(__name__)

app.register_blueprint(blueprint=algs_blu)


def thread_1():
    app.run(debug=False, port=5000)


def thread_2():
    mqListen()


def run_app():
    app.run(debug=False, port=5000)
