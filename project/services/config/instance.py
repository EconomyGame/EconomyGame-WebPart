from .controllers import api


def register_config(app):
    app.add_namespace(api, path='/config')
