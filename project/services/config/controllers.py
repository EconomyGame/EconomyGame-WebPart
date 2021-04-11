from flask_restplus import Namespace, Resource, fields
from flask import request

from project.app import serializer
from project.decorators import auth_secure, admin_secure
from project.utils.mongo import fetch_config
from project.utils.game import update_balance


api = Namespace('Config', description='Config service')


@api.route('/fetch_config')
class FetchConfig(Resource):
    def get(self):
        return serializer.jsonify(fetch_config())


@api.route('/inc_balance')
@api.doc(security=['session_token', 'game_id', "admin_token"])
class IncBalance(Resource):
    balance_model = api.model(
        'Inc Balance input',
        {
            'balance': fields.Integer('INC of balance')
        },
    )

    @api.expect(balance_model)
    @auth_secure
    @admin_secure
    def post(self):
        session_token = request.headers.get('Authorization')
        game_id = request.headers.get('Game')
        balance = request.json.get("balance")

        try:
            _request = update_balance(game_id, session_token, balance)
            if not _request["status"]:
                return serializer.jsonify({"status": False, "message": "Update Balance error"})

            return serializer.jsonify(_request)
        except Exception as D:
            print(D)
            return serializer.jsonify({"status": False, "message": "Unknown error"})