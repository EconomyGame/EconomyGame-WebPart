from project.app import socketio, app


def broadcast_game(game_object):
    print(game_object)
    game_object = prepare_gameobject(game_object)
    socketio.emit('update_game', game_object, broadcast=True)


def prepare_gameobject(game_object):
    game_object["_id"] = str(game_object["_id"])
    return game_object
