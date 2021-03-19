from flask_restplus import Namespace, Resource
from flask import request

from project.app import serializer
from project.decorators import auth_secure
from project.utils.game import create_game, join_game, fetch_game, is_ready_update, leave_game


api = Namespace('Game Lobby', description='Game Lobby service')


@api.route('/create_game')
class CreateGame(Resource):
    def post(self):
        try:
            _request = create_game()
            if not _request["status"]:
                return serializer.jsonify({"status": False, "message": "Game creation error"})

            return serializer.jsonify(_request)
        except Exception as D:
            print(D)
            return serializer.jsonify({"status": False, "message": "Unknown error"})


@api.route('/join_game')
@api.doc(
    params={
        'ref_code': {
            'description': 'Unique code of the game session',
            'in': 'query',
            'type': 'string',
            'required': True,
        }
    }
)
class JoinGame(Resource):
    def get(self):
        ref_code = request.args.get('ref_code')
        try:
            _request = join_game(ref_code)

            return serializer.jsonify(_request)
        except Exception as D:
            print(D)
            return serializer.jsonify({"status": False, "message": "Unknown error"})


@api.route('/fetch_game')
@api.doc(security=['session_token', 'game_id'])
class FetchGame(Resource):
    @auth_secure
    def get(self):
        session_token = request.headers.get('Authorization')
        game_id = request.headers.get('Game')

        return serializer.jsonify(fetch_game(game_id, session_token))


@api.route('/update_ready')
@api.doc(security=['session_token', 'game_id'])
class UpdateReady(Resource):
    @auth_secure
    def get(self):
        session_token = request.headers.get('Authorization')
        game_id = request.headers.get('Game')

        return serializer.jsonify(is_ready_update(game_id, session_token))


@api.route('/leave_game')
@api.doc(security=['session_token', 'game_id'])
class LeaveGame(Resource):
    @auth_secure
    def get(self):
        session_token = request.headers.get('Authorization')
        game_id = request.headers.get('Game')

        return serializer.jsonify(leave_game(game_id, session_token))
