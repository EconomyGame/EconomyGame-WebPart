from datetime import timedelta
import datetime
from bson.objectid import ObjectId

from project.utils.standart.mongo import fetch_game_by_code, fetch_game_by_id, insert_game, update_game, fetch_config
from project.utils.objects.user import new_user
from project.utils.standart.common import get_random_string, get_user_ind
from project.utils.objects.city import generate_cities
from project.utils.objects.source import generate_sources
from project.sockets import broadcast_game


def create_game(username, cfg=None):
    """Создание игры, выдача token для leader, etc"""
    user = new_user(username)
    if cfg is None:
        cfg = fetch_config()
    del cfg["_id"]
    data = {
        "is_started": False,
        "ref_code": generate_unique_code(),
        "users": [user],
        "factories": [],
        "cities": [],
        "sources": [],
        "datetime": datetime.datetime.utcnow().isoformat()
    }
    game_id = insert_game(data)
    data["_id"] = ObjectId(game_id)
    return dict(status=True, user=user, game=data, cfg=cfg)


def join_game(ref_code, username, cfg=None):
    """
    Подключение к сущестующей сессии

    Требуется параметр ref_code
    """

    game = fetch_game_by_code(ref_code)
    if cfg is None:
        cfg = fetch_config()

    try:
        validate_to_join(game_object=game, username=username, config=cfg)

        user = new_user(username=username)
        game["users"].append(user)
        update_game(str(game["_id"]), game)
        broadcast_game(game)

        response = dict(status=True, game=game, user=user, cfg=cfg)
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
        broadcast_game(game)

        response = dict(status=True, game=game)
    except AssertionError:
        response = dict(status=False, message='Validation Error')

    return response


def is_ready_update(game_id, session_token):
    """Обновление флага is_ready игрока с session_token в игре game_id"""
    game = fetch_game_by_id(game_id)

    user_ind = get_user_ind(game, session_token)
    game["users"][user_ind]["is_ready"] = not game["users"][user_ind]["is_ready"]
    update_game(str(game["_id"]), game)
    broadcast_game(game)

    return dict(status=True, game=game, user=game["users"][user_ind])


def leave_game(game_id, session_token):
    """Выход из игровой сессии"""
    game = fetch_game_by_id(game_id)

    user_ind = get_user_ind(game, session_token)
    game["users"].pop(user_ind)
    update_game(str(game_id), game)
    broadcast_game(game)

    return dict(status=True, game=game)


def fetch_game(game_id, session_token):
    """Поиск игры"""

    game = fetch_game_by_id(game_id)

    user_ind = get_user_ind(game, session_token)

    return dict(status=True, game=game, user=game["users"][user_ind])


def update_balance(game_id, session_token, balance):
    """INC of user balance"""
    game = fetch_game_by_id(game_id)
    user_ind = get_user_ind(game, session_token)

    game["users"][user_ind]["balance"] += balance
    update_game(str(game_id), game)
    broadcast_game(game)

    return dict(status=True, game=game)


def generate_unique_code():
    """Генерация уникального кода, который еще не использовался или устарел"""
    code = get_random_string(5)
    game = fetch_game_by_code(code)
    while game is not None and datetime.datetime.fromisoformat(game["datetime"]) +\
            timedelta(hours=6) > datetime.datetime.utcnow():
        code = get_random_string(5)
    return code


def validate_to_join(game_object, username, config):
    """Валидация игровой сессии"""
    try:
        assert game_object is not None
        assert datetime.datetime.fromisoformat(game_object["datetime"]) +\
               timedelta(hours=2) >= datetime.datetime.utcnow()
        assert len(game_object["users"]) < config["count_users"]
        assert game_object["is_started"] is False
        assert username not in list(map(lambda x: x["username"], game_object["users"]))
    except KeyError:
        raise AssertionError


def validate_to_start(game_object,):
    """Валидация готовности игры к старту"""
    try:
        assert all(map(lambda x: x["is_ready"], game_object["users"]))
        assert game_object["is_started"] is False
    except KeyError:
        raise AssertionError
