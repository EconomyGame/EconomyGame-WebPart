from flask_restplus import Namespace, Resource

from project.app import serializer
from project.utils.mongo import fetch_config


api = Namespace('Config', description='Config service')


@api.route('/fetch_config')
class FetchConfig(Resource):
    def get(self):
        return serializer.jsonify(fetch_config())
