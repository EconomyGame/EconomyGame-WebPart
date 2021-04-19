from project.app import socketio


@socketio.on('connect')
def socketio_connect():
    print(f'New connection!')


@socketio.on('disconnect')
def socketio_disconnect():
    print(f'User has been disconnected')
