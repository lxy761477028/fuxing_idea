from flask import Flask
from Api.url_dispatch import algs_blu
from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

app.register_blueprint(blueprint=algs_blu)

def run_app():
    app.run(debug=False, port=Config.PORT)

# run_app()