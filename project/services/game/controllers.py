from flask_restplus import Namespace, Resource

from project.app import serializer
from project.utils.mongo import fetch_config
from project.utils.game import create_game


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
