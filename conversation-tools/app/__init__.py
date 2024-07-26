from flask import Flask
from app.routes import conversation_tools


def create_app():
    app = Flask(__name__)
    app.register_blueprint(conversation_tools)
    return app
