import random
import os
import string

from project.utils.standart.mongo import fetch_game_by_id, fetch_config
from project import config


config_object = getattr(config, os.environ['APP_SETTINGS'])


def get_random_string(size=10):
    """Генерация рандомной строки из цифр и ascii символов длиной size"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(size))


def check_auth(request):
    """Проверка авторизации по request"""
    session_token = request.headers.get('Authorization')
    game_id = request.headers.get('Game')

    game = fetch_game_by_id(game_id)
    if game is not None and session_token in list(map(lambda x: x["session_token"], game["users"])):
        return game
    else:
        return


def check_admin_auth(request):
    """Проверка ADMIN авторизации по request"""
    admin_token = request.headers.get('ADMIN')
    return admin_token == config_object.ADMIN_SECRET_KEY


def validate_coords(game, coords):
    if game is None:
        return False

    used = [x["coords"] for x in game["cities"]] + \
           [x["coords"] for x in game["sources"]] + \
           [x["coords"] for x in game["factories"]]
    return list(coords) not in used


def get_transfer_fee(coords_1, coords_2, cfg=None):
    if cfg is None:
        cfg = fetch_config()
    return (abs(coords_1[0] - coords_2[0]) + abs(coords_1[1] - coords_2[1])) * cfg["transfer_price"]


def get_user_ind(game, session_token):
    res_find = [x["session_token"] == session_token for x in game["users"]]
    try:
        return res_find.index(True)
    except ValueError as D:
        return -1


def get_factory_ind(game, factory_id):
    res_find = [x["_id"] == factory_id for x in game["factories"]]
    try:
        return res_find.index(True)
    except ValueError as D:
        return -1


def get_city_ind(game, city_id):
    res_find = [x["_id"] == city_id for x in game["cities"]]
    try:
        return res_find.index(True)
    except ValueError as D:
        return -1


def get_source_ind(game, source_id):
    res_find = [x["_id"] == source_id for x in game["sources"]]
    try:
        return res_find.index(True)
    except ValueError as D:
        return -1
