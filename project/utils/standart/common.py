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


def get_user(game, session_token):
    user_ind = get_user_ind(game, session_token)
    return game["users"][user_ind]


def get_user_by_username(game, username):
    for i in game["users"]:
        if i["username"] == username:
            return i


def get_factory(game, factory_id):
    factory_id = get_factory_ind(game, factory_id)
    return game["factories"][factory_id]


def get_city(game, city_id):
    city_id = get_city_ind(game, city_id)
    return game["cities"][city_id]


def get_source(game, source_id):
    source_id = get_source_ind(game, source_id)
    return game["sources"][source_id]


def get_user_factories(game, username):
    """Получение списка заводов игрока"""
    factories = game["factories"]
    return list(filter(lambda x: x["username"] == username, factories))


def get_factories_near_source(game, source_id):
    """Получение списка заводов подключенных к источнику"""
    factories = game["factories"]
    return list(filter(lambda x: x["source_id"] == source_id, factories))


def get_factories_near_city(game, city_id):
    """Получение списка заводов подключенных к источнику"""
    factories = game["factories"]
    return list(filter(lambda x: x["city_id"] == city_id, factories))


def get_str_level_factory(factory):
    """Преобразовать уровень завода в строковый вид"""
    return "level_" + str(factory["level"])


def get_level_diff(factory, city, cfg):
    """Разница в уровне ресурса города и фабрики"""
    return factory["level"] - city["resource_levels"][get_name_resource(factory, cfg)]


def get_name_resource(factory, cfg):
    """Получить название ресурса у фабрики"""
    resource_id = factory["resource_id"]
    for i in cfg["resource_ids"]:
        if cfg["resource_ids"][i] == resource_id:
            return i


def get_profit_multi(level_diff, cfg):
    """Мультипликатор выплаты от города"""
    rates_dif = cfg["cities"]["rates_dif"]
    return rates_dif ** level_diff


def get_city_payout(products, mult, cfg):
    """Выплата города"""
    return cfg["cities"]["city_payout"] * mult * products
