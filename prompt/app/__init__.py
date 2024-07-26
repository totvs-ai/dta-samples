from flask import Flask
from app.routes import prompt


def create_app():
    app = Flask(__name__)
    app.register_blueprint(prompt)
    return app
