from datetime import datetime as dt

from project.utils.mongo import fetch_game_by_id, fetch_config, update_game
from project.utils.common import validate_coords, get_random_string, get_user_ind, get_factory_ind, get_city_ind, get_source_ind
from project.sockets import broadcast_game


def make_factory(game_id, session_token, data, cfg=None):
    """Создание фабрики"""

    if cfg is None:
        cfg = fetch_config()

    game = fetch_game_by_id(game_id)
    user_ind = get_user_ind(game, session_token)
    user = game["users"][user_ind]

    if not validate_coords(game, data["coords"]):
        return dict(status=False, message="Coords error")

    if not validate_balance(user, cfg["factories"]["price_factory"]):
        return dict(status=False, message="Price error")

    factory = {
        "_id": get_random_string(40),
        "username": user["username"],
        "resource_id": data["resource_id"],
        "coords": data["coords"],
        "city_id": None,
        "source_id": None,
        "level": 1,
        "coef": cfg["factories"]["start_coef"],
        "datetime": dt.utcnow().isoformat()
    }

    game["users"][user_ind]["balance"] -= cfg["factories"]["price_factory"]
    game["factories"].append(factory)
    update_game(str(game["_id"]), game)
    broadcast_game(game)

    return dict(status=True, game=game, factory=factory)


def upgrade_factory(game_id, session_token, data, cfg=None):
    """Апгрейд фабрики"""

    if cfg is None:
        cfg = fetch_config()

    game = fetch_game_by_id(game_id)

    user_ind = get_user_ind(game, session_token)
    user = game["users"][user_ind]

    factory_id = get_factory_ind(game, data["factory_id"])
    factory = game["factories"][factory_id]

    if not validate_owner(user, factory):
        return dict(status=False, message="Access error")

    now_level = factory["level"]
    key_level = "level_" + str(now_level)

    if not validate_balance(user, cfg["factories"]["factory_levels"][key_level]):
        return dict(status=False, message="Price error")

    factory["level"] += 1
    factory["coef"] *= cfg["factories"]["start_coef"]

    game["users"][user_ind]["balance"] -= cfg["factories"]["factory_levels"][key_level]
    game["factories"][factory_id] = factory
    update_game(str(game["_id"]), game)
    broadcast_game(game)

    return dict(status=True, game=game, factory=factory)


def select_source(game_id, session_token, data):
    """ВЫбор источника добычи"""

    game = fetch_game_by_id(game_id)

    user_ind = get_user_ind(game, session_token)
    user = game["users"][user_ind]

    factory_id = get_factory_ind(game, data["factory_id"])
    factory = game["factories"][factory_id]

    if not validate_owner(user, factory):
        return dict(status=False, message="Access error")

    source_id = get_source_ind(game, data["source_id"])
    source = game["sources"][source_id]

    if not validate_resource(factory, source):
        return dict(status=False, message="Source error")

    factory["source_id"] = source["_id"]

    game["factories"][factory_id] = factory
    update_game(str(game["_id"]), game)
    broadcast_game(game)

    return dict(status=True, game=game, factory=factory)


def select_city(game_id, session_token, data):
    """ВЫбор города для поставки"""

    game = fetch_game_by_id(game_id)

    user_ind = get_user_ind(game, session_token)
    user = game["users"][user_ind]

    factory_id = get_factory_ind(game, data["factory_id"])
    factory = game["factories"][factory_id]

    if not validate_owner(user, factory):
        return dict(status=False, message="Access error")

    city_id = get_city_ind(game, data["city_id"])
    city = game["cities"][city_id]

    factory["city_id"] = city["_id"]

    game["factories"][factory_id] = factory
    update_game(str(game["_id"]), game)
    broadcast_game(game)

    return dict(status=True, game=game, factory=factory)


def validate_balance(user, price):
    return user["balance"] >= price


def validate_owner(user, factory):
    return user["username"] == factory["username"]


def validate_resource(factory, source):
    return factory["resource_id"] == source["resource_id"]
