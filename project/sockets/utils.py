from project.app import socketio, app


def broadcast_game(prepared_game_object):
    print(prepared_game_object)
    socketio.emit('update_game', prepared_game_object, broadcast=True)
