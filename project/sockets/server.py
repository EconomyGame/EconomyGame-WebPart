from project.app import socketio, app
from project.app import serializer
from project.utils.mongo import fetch_game_by_id


@socketio.on('connect')
def socketio_connect():
    print(f'New connection!')


@socketio.on('disconnect')
def socketio_disconnect():
    print(f'User has been disconnected')


@app.route("/test_socket/<game_id>")
def test_socket(game_id):
    game = fetch_game_by_id(game_id)
    game["_id"] = str(game["_id"])
    print(game)
    socketio.emit('update_game', {}, broadcast=True)
    return "OK"
