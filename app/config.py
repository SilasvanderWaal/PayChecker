import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-insecure-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )

class DevelopmentConfig(BaseConfig):
        DEBUG = True

class ProductionConfig(BaseConfig):
        DEBUG = False

config_by_name = {
    "development" : DevelopmentConfig,
    "production" : ProductionConfig,
}
