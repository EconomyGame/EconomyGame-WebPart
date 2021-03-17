from .controllers import api


def register_game_lobby(app):
    app.add_namespace(api, path='/game_lobby')
