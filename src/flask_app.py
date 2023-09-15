# This file is used in Docker only
from flask import Flask, request

from src.api import handle_api_event


def create_app():
    app = Flask("src.flask_app")

    @app.post("/")
    def handle_event():
        return handle_api_event(request)

    return app


application = create_app()
