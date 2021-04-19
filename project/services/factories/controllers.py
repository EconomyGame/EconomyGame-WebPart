from flask_restplus import Namespace, Resource, fields
from flask import request

from project.app import serializer
from project.decorators import auth_secure
from project.utils.objects.factory import make_factory, upgrade_factory, select_city, select_source


api = Namespace('Game Factories', description='Game Factories service')


@api.route('/make_factory')
@api.doc(security=['session_token', 'game_id'])
class CreateFactory(Resource):
    factory_model = api.model(
        'Create Factory input',
        {
            'resource_id': fields.Integer('ID of resource, int in range [1, 4]'),
            'coords': fields.String('List, format [x, y]')
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


@api.route('/upgrade_factory')
@api.doc(security=['session_token', 'game_id'])
class UpgradeFactory(Resource):
    upgrade_model = api.model(
        'Upgrade Factory input',
        {
            'factory_id': fields.String('ID of our factory')
        },
    )

    @auth_secure
    @api.expect(upgrade_model)
    def post(self):
        session_token = request.headers.get('Authorization')
        game_id = request.headers.get('Game')
        data = request.json

        try:
            _request = upgrade_factory(game_id, session_token, data)
            if not _request["status"]:
                return serializer.jsonify({"status": False, "message": "Factory upgrade error"})

            return serializer.jsonify(_request)
        except Exception as D:
            print(D)
            return serializer.jsonify({"status": False, "message": "Unknown error"})


@api.route('/select_city')
@api.doc(security=['session_token', 'game_id'])
class SelectCityFactory(Resource):
    city_model = api.model(
        'Select City input',
        {
            'factory_id': fields.String('ID of our factory'),
            'city_id': fields.String('ID of our city')
        },
    )

    @auth_secure
    @api.expect(city_model)
    def post(self):
        session_token = request.headers.get('Authorization')
        game_id = request.headers.get('Game')
        data = request.json

        try:
            _request = select_city(game_id, session_token, data)
            if not _request["status"]:
                return serializer.jsonify(_request)

            return serializer.jsonify(_request)
        except Exception as D:
            print(D)
            return serializer.jsonify({"status": False, "message": "Unknown error"})


@api.route('/select_source')
@api.doc(security=['session_token', 'game_id'])
class SelectSourceFactory(Resource):
    source_model = api.model(
        'Select Source input',
        {
            'factory_id': fields.String('ID of our factory'),
            'source_id': fields.String('ID of our source')
        },
    )

    @auth_secure
    @api.expect(source_model)
    def post(self):
        session_token = request.headers.get('Authorization')
        game_id = request.headers.get('Game')
        data = request.json

        try:
            _request = select_source(game_id, session_token, data)
            if not _request["status"]:
                return serializer.jsonify(_request)

            return serializer.jsonify(_request)
        except Exception as D:
            print(D)
            return serializer.jsonify({"status": False, "message": "Unknown error"})