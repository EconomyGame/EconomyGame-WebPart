from flask_restplus import Namespace, Resource, fields
from flask import request

from project.app import serializer
from project.decorators import auth_secure
from project.utils.factory import make_factory


api = Namespace('Game Factories', description='Game Factories service')


@api.route('/make_factory')
class CreateFactory(Resource):
    factory_model = api.model(
        'Create Factory input',
        {
            'resource_id': fields.List('ID of resource, int in range [1, 4]'),
            'coords': fields.List('Coords format [x, y]')
        },
    )

    @auth_secure
    @api.expect(factory_model)
    def post(self):
        session_token = request.headers.get('Authorization')
        game_id = request.headers.get('Game')
        data = request.json

        try:
            _request = make_factory(game_id, session_token, data)
            if not _request["status"]:
                return serializer.jsonify({"status": False, "message": "Factory creation error"})

            return serializer.jsonify(_request)
        except Exception as D:
            print(D)
            return serializer.jsonify({"status": False, "message": "Unknown error"})