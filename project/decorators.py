import os
from functools import wraps
from flask import request

from project import config
from .utils.standart import check_auth, check_admin_auth


config_object = getattr(config, os.environ['APP_SETTINGS'])


def auth_secure(f):
    """Обычная валидация авторизованности"""

    @wraps(f)
    def wrapped(*args, **kwargs):
        if check_auth(request) is None:
            return dict(message='Authentication Error'), 401
        return f(*args, **kwargs)

    return wrapped


def admin_secure(f):
    """Админская валидация авторизованности"""

    @wraps(f)
    def wrapped(*args, **kwargs):
        if check_admin_auth(request) is False:
            return dict(message='Authentication Error'), 401
        return f(*args, **kwargs)

    return wrapped
