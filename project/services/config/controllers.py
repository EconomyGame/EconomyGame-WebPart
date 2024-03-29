from flask_restplus import Namespace, Resource, fields
from flask import request

from project.app import serializer
from project.decorators import auth_secure, admin_secure
from project.utils.standart.mongo import fetch_config, get_active_games
from project.utils.objects.game import update_balance, stop_game


api = Namespace('Config', description='Config service')


@api.route('/fetch_config')
class FetchConfig(Resource):
    def get(self):
        return serializer.jsonify(fetch_config())


@api.route('/active_games')
class ActiveGames(Resource):
    def get(self):
        games = get_active_games()
        for i in games:
            i["_id"] = str(i["_id"])
        return serializer.jsonify(games)


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


@api.route('/stop_game')
@api.doc(security=['game_id', "admin_token"])
class StopGame(Resource):
    @admin_secure
    def post(self):
        game_id = request.headers.get('Game')

        try:
            _request = stop_game(game_id)
            if not _request["status"]:
                return serializer.jsonify({"status": False, "message": "Stop Game error"})

            return serializer.jsonify(_request)
        except Exception as D:
            print(D)
            return serializer.jsonify({"status": False, "message": "Unknown error"})
