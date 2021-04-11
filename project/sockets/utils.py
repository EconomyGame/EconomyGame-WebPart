from project.app import socketio, app
from project.utils.game import delete_sessions_from_game


def broadcast_game(game_object):
    game_object = prepare_gameobject(game_object)
    socketio.emit('update_game', game_object, broadcast=True)


def prepare_gameobject(game_object):
    game_object["_id"] = str(game_object["_id"])
    game_object = delete_sessions_from_game(game_object)
    return game_object
