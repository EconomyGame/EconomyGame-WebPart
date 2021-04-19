from flask_restplus import Namespace, Resource, fields
from flask import request

from project.app import serializer
from project.decorators import auth_secure
from project.utils.objects.game import create_game, join_game, fetch_game, is_ready_update, leave_game, start_game


api = Namespace('Game Lobby', description='Game Lobby service')


@api.route('/create_game')
class CreateGame(Resource):
    game_model = api.model(
        'Create Game input',
        {
            'username': fields.String('Player username for this game')
        },
    )

    @api.expect(game_model)
    def post(self):
        username = request.json.get("username")
        try:
            _request = create_game(username=username)
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
        },
        'username': {
            'description': 'Player name',
            'in': 'query',
            'type': 'string',
            'required': True,
        }
    }
)
class JoinGame(Resource):
    def get(self):
        ref_code = request.args.get('ref_code')
        username = request.args.get('username')
        try:
            _request = join_game(ref_code, username)

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


@api.route('/start_game')
@api.doc(security=['session_token', 'game_id'])
class StartGame(Resource):
    @auth_secure
    def get(self):
        game_id = request.headers.get('Game')

        return serializer.jsonify(start_game(game_id))
