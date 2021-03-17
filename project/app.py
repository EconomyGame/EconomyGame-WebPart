from flask_pymongo import PyMongo
from flask_cors import CORS
from flask import Flask, Blueprint
import os

from project import config
from project.extensions import ExtendedApi
from project.utils.const import swagger_authorizations
from project.utils.serialize import Serializer


app = Flask(__name__, subdomain_matching=True)
app.config.from_object(getattr(config, os.environ['APP_SETTINGS']))
app.secret_key = app.config['FLASK_SECRET_KEY']

api_blueprint = Blueprint('Game API', __name__)

api = ExtendedApi(
    api_blueprint,
    title='Game API documentation',
    version='1.0',
    description='TP-PROJECT.gameapi spec',
    doc='/docs/',
    authorizations=swagger_authorizations,
)
app.register_blueprint(api_blueprint, url_prefix='/api/v1')


mongo = PyMongo(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
serializer = Serializer(app)


from .errorhandlers import *
from project.services.config.instance import register_config

register_config(api)


if __name__ == '__main__':
    app.run()