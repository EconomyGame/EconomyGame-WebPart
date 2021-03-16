import requests
from hashlib import sha256
from hmac import new as hash_hmac
from datetime import datetime as dt
from datetime import timedelta
from bson.objectid import ObjectId

from project.utils.const import config_object
from project.utils.mongo import fetch_game_by_code, fetch_game_by_id, insert_game, update_game
from project.utils.user import new_user
from project.utils.common import get_random_string


def create_game():
    """Создание игры, выдача token для leader, etc"""
    user = new_user()
    data = {
        "is_started": False,
        "ref_code": generate_unique_code(),
        "users": [user],
        "factories": [],
        "cities": [],
        "sources": [],
        "datetime": dt.utcnow().isoformat()
    }
    game_id = insert_game()
    data["_id"] = ObjectId(game_id)

    return dict(status=True, user=user, game=data)


def join_game(ref_code):
    """
    Подключение к сущестующей сессии

    Требуется параметр ref_code
    """

    game = fetch_game_by_code(ref_code)
    try:
        validate_game(game)

        user = new_user()
        game["users"].append(user)
        update_game(game)

        response = dict(status=True, game=game, user=user)
    except AssertionError:
        response = dict(status=False, message='Validation Error')

    return response


def generate_unique_code():
    """Генерация уникального кода, который еще не использовался или устарел"""
    code = get_random_string(5)
    game = fetch_game_by_code(code)
    while game is None or dt.fromisoformat(game["datetime"]) + timedelta(hours=6) < dt.utcnow():
        code = get_random_string(5)
    return code


def validate_game(game_object):
    """Валидация игровой сессии"""
    try:
        assert game_object is None
        assert dt.fromisoformat(game_object["datetime"]) + timedelta(hours=2) < dt.utcnow()
    except KeyError:
        raise AssertionError
