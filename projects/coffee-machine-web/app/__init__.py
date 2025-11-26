# app/__init__.py
import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from config import Config
from .database import init_db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init DB
    init_db(app)

    # Logging setup
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/coffee.log", maxBytes=10240, backupCount=5
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("CoffeeMachine startup")

    # Register routes
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

