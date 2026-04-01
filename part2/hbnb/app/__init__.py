from flask import Flask
from app.api import init_api


def create_app():
    app = Flask(__name__)
    init_api(app)
    return app
