from project.app import socketio, app
from copy import deepcopy


def broadcast_game(game_object):
    g_copy = deepcopy(game_object)
    g_copy = prepare_gameobject(g_copy)
    socketio.emit('update_game', g_copy, broadcast=True)


def prepare_gameobject(game_object):
    game_object["_id"] = str(game_object["_id"])
    for i in
    return game_object
