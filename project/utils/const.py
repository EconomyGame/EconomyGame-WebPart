import os

from project import config


config_object = getattr(config, os.environ['APP_SETTINGS'])
swagger_authorizations = {
    'session_token': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'game_id': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Game'
    },
}
