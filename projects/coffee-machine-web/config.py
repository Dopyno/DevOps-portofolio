# config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    DATABASE = os.environ.get(
        "DATABASE_URL",
        os.path.join(BASE_DIR, "coffee.db")
    )
    S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
    AWS_REGION = os.environ.get("AWS_REGION", "eu-west-1")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

