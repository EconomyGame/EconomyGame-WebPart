from flask_socketio import SocketIO
from flask import Flask
import datetime

app = Flask(__name__)
app.config['PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
socketio = SocketIO(app)


@socketio.on('connect')
def socketio_connect():
    print(f'New connection!')


@socketio.on('disconnect')
def socketio_disconnect():
    print(f'User has been disconnected')


@app.route("/test_socket")
def test_socket():
    socketio.emit('update_game', {}, broadcast=True)
    return "OK"


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=443, max_size=1024)
