from datetime import timedelta
import datetime
from bson.objectid import ObjectId

from project.utils.mongo import fetch_game_by_code, fetch_game_by_id, insert_game, update_game, fetch_config
from project.utils.user import new_user
from project.utils.common import get_random_string
from project.utils.city import generate_cities
from project.utils.source import generate_sources


def create_game(cfg=None):
    """Создание игры, выдача token для leader, etc"""
    user = new_user()
    if cfg is None:
        cfg = fetch_config()
    del cfg["_id"]
    data = {
        "is_started": False,
        "ref_code": "sevatest",
        "users": [user],
        "factories": [],
        "cities": [],
        "sources": [],
        "datetime": datetime.datetime.utcnow().isoformat()
    }
    game_id = insert_game(data)
    data["_id"] = ObjectId(game_id)
    return dict(status=True, user=user, game=data, cfg=cfg)


def join_game(ref_code, cfg=None):
    """
    Подключение к сущестующей сессии

    Требуется параметр ref_code
    """

    game = fetch_game_by_code(ref_code)
    if cfg is None:
        cfg = fetch_config()

    try:
        validate_game(game_object=game, config=cfg)

        user = new_user()
        game["users"].append(user)
        update_game(str(game["_id"]), game)

        response = dict(status=True, game=game, user=user)
    except AssertionError:
        response = dict(status=False, message='Validation Error')

    return response


def start_game(game_id, cfg=None):
    """Запуск игры"""
    game = fetch_game_by_id(game_id)
    if cfg is None:
        cfg = fetch_config()

    try:
        validate_to_start(game_object=game)

        game["cities"] = generate_cities(cfg=cfg)
        game["sources"] = generate_sources(cfg=cfg)
        game["is_started"] = True
        update_game(str(game["_id"]), game)

        response = dict(status=True, game=game)
    except AssertionError:
        response = dict(status=False, message='Validation Error')

    return response


def generate_unique_code():
    """Генерация уникального кода, который еще не использовался или устарел"""
    code = get_random_string(5)
    game = fetch_game_by_code(code)
    while game is not None and datetime.datetime.fromisoformat(game["datetime"]) +\
            timedelta(hours=6) > datetime.datetime.utcnow():
        code = get_random_string(5)
    return code


def validate_game(game_object, config):
    """Валидация игровой сессии"""
    try:
        assert game_object is None
        assert datetime.datetime.fromisoformat(game_object["datetime"]) +\
               timedelta(hours=2) < datetime.datetime.utcnow()
        assert len(game_object["users"]) >= config["count_users"]
    except KeyError:
        raise AssertionError


def validate_to_start(game_object,):
    """Валидация готовности игры к старту"""
    try:
        assert all(map(lambda x: x["is_ready"], game_object["users"])) is False
    except KeyError:
        raise AssertionError
