import os
from functools import wraps
from flask import request

from project import config
from .utils.common import check_auth


config_object = getattr(config, os.environ['APP_SETTINGS'])


def auth_secure(f):
    """Обычная валидация авторизованности"""

    @wraps(f)
    def wrapped(*args, **kwargs):
        print("validate stage #1")
        if check_auth(request) is None:
            return dict(message='Authentication Error'), 401
        return f(*args, **kwargs)

    return wrapped
