import os

from decouple import config
from gwap_framework.redis import RedisServer
from gwap_framework.utils.encoders import UUIDEncoder

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = config('DEBUG', cast=bool)
AUTO_RELOAD = config('AUTO_RELOAD', cast=bool)
PORT = config('PORT', cast=int)
HOST = config('HOST')

GWA_ENVIRONMENT = config('GWA_ENVIRONMENT')
GWA_KEY = config('GWA_KEY')


class GWAAppConfig:

    def __init__(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConfig.get_uri()
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['RESTFUL_JSON'] = {'cls': UUIDEncoder}
        app.config['ELASTIC_APM'] = {
            'SERVICE_NAME': ElasticApmConfig.SERVICE_NAME,
            'SECRET_TOKEN': ElasticApmConfig.SECRET_TOKEN,
            'SERVER_URL': ElasticApmConfig.SERVER_URL,
            'DEBUG': DEBUG,
        }


class ElasticApmConfig:
    SERVICE_NAME = config('ELASTIC_APM_SERVICE_NAME')
    SECRET_TOKEN = config('ELASTIC_APM_SECRET_TOKEN')
    SERVER_URL = config('ELASTIC_APM_SERVER_URL')


class DatabaseConfig:
    DB_HOST = config('DB_HOST')
    DB_HOST_REPLICA = config('DB_HOST_REPLICA')
    DB_USER = config('DB_USER')
    DB_PASSWORD = config('DB_PASSWORD')
    DB_NAME = config('DB_NAME')

    @staticmethod
    def get_uri(read_replica=False):
        if not read_replica:
            return f"postgresql://{DatabaseConfig.DB_USER}:{DatabaseConfig.DB_PASSWORD}@{DatabaseConfig.DB_HOST}/{DatabaseConfig.DB_NAME}"
        return f"postgresql://{DatabaseConfig.DB_USER}:{DatabaseConfig.DB_PASSWORD}@{DatabaseConfig.DB_HOST_REPLICA}/{DatabaseConfig.DB_NAME}"


class LoggerSettings:
    LOGGER_NAME = f"gwa-{GWA_KEY}"
    LOGGER_APPLICATION = f"{GWA_KEY}"
    LOGGER_PRODUCT = f"gwa"
    LOGGER_OUTPUT_FORMAT = 'JSON'


class PubSubSettings:
    HOST = config('PUB_SUB_HOST')
    PORT = config('PUB_SUB_PORT')
    TOPICS = {
        'GOAL': f'{GWA_ENVIRONMENT}-{GWA_KEY}-exercises'
    }


class Cache(RedisServer):
    REDIS_HOST = config('CACHE_HOST')
    REDIS_PORT = config('CACHE_PORT')
