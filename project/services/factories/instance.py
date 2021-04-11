from .controllers import api


def register_game_factories(app):
    app.add_namespace(api, path='/game_factories')
