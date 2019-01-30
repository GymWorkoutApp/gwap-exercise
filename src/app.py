import logging

from flask import Blueprint
from flask_cors import CORS
from gwap_framework.api import GwapApi
from gwap_framework.app import GwapApp
from gwap_framework.auth import GwapAuth
from gwap_framework.errors import GwapErrorHandlerConfig
from gwap_framework.resource import HealthCheckResource

from src.database import db
from src.resources import resources_v1
from src.settings import PORT, DEBUG, GWAAppConfig, HOST, GWA_KEY


def create_app():
    new_app = GwapApp(__name__, static_folder=None)
    GWAAppConfig(new_app)
    GwapErrorHandlerConfig(new_app)
    # ElasticAPM(new_app, logging=True)
    CORS(new_app)
    db.init_app(new_app)

    api = GwapApi(new_app, prefix=f"/gwap/{GWA_KEY}")
    api.add_resource(HealthCheckResource, '/')

    # version 1
    bp_v1 = Blueprint('v1', __name__, url_prefix=f"/gwap/{GWA_KEY}/v1")
    GwapAuth(bp_v1, new_app.logger)
    GwapErrorHandlerConfig(bp_v1)
    api_v1 = GwapApi(bp_v1)
    new_app.register_blueprint(bp_v1)

    for resource_v1 in resources_v1:
        api_v1.add_resource(resource_v1['resource'], *resource_v1['urls'], endpoint=resource_v1['endpoint'],
                            methods=resource_v1['methods'])

    return new_app


app = create_app()

if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    app.run(debug=DEBUG, port=PORT, host=HOST)
