import os

from project import config


config_object = getattr(config, os.environ['APP_SETTINGS'])
swagger_authorizations = {
    'token': {
        'type': 'userToken',
        'in': 'header',
        'name': 'Authorization'
    }
}
