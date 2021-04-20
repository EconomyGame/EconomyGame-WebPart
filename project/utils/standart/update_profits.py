from .common import get_user_factories, get_transfer_fee, get_city, get_user_ind, get_source, get_factory,\
    get_str_level_factory, get_level_diff, get_profit_multi, get_city_payout, get_factories_near_source,\
    get_user_by_username, get_source_ind, get_factories_near_city, get_name_resource, get_user_by_username
from .mongo import fetch_config, update_game


def update_factory(game, factory, cfg=None):
    """Обновление фабрики и всего всего окружающего"""

    if cfg is None:
        cfg = fetch_config()

    if factory["city_id"] is not None:
        game = update_city(game, get_city(game, factory["city_id"]), cfg)
    if factory["source_id"] is not None:
        game = update_source(game, get_source(game, factory["source_id"]), cfg)
    game = update_player(game, get_user_by_username(game, factory["username"]), cfg)
    return game


def update_city(game, city, cfg=None):
    """Давайте обновим город и всех игроков, подключенных к нему"""

    if cfg is None:
        cfg = fetch_config()

    factories = get_factories_near_city(game, city["_id"])
    user_list = []

    for i in city["resource_delta"]:
        city["resource_delta"][i] = 0

    for i in factories:
        if i["username"] not in user_list:
            user_list.append(i["username"])
        if get_factory_profit(game, i, cfg) != 0:
            city["resource_delta"][get_name_resource(i, cfg)] += get_factory_deliver(city, i, cfg)

    for i in city["resource_delta"]:
        if city["resource_delta"][i] == 0:
            city["resource_delta"][i] = cfg["cities"]["requied_levels"]["level_" + str(city["resource_levels"][i])]

    for i in user_list:
        game = update_player(game, get_user_by_username(game, i), cfg)

    return game


def update_source(game, source, cfg=None):
    """Давайте обновим источник и всех игроков, подключенных к нему"""

    if cfg is None:
        cfg = fetch_config()

    factories = get_factories_near_source(game, source["_id"])
    new_delta = 0
    city_list = []
    for i in factories:
        if get_factory_profit(game, i, cfg) != 0:
            new_delta += cfg["max_products"][get_str_level_factory(i)]
            if i["city_id"] not in city_list:
                city_list.append(i["city_id"])

    source_ind = get_source_ind(game, source["_id"])
    game["sources"][source_ind]["delta"] = new_delta

    for i in city_list:
        game = update_city(game, get_city(game, i), cfg)

    return game


def update_player(game, user, cfg):
    """Давайте обновим игрока и пересчитаем его"""

    if cfg is None:
        cfg = fetch_config()

    factories = get_user_factories(game, user["username"])
    user_profit = 0
    for i in factories:
        user_profit += get_factory_profit(game, i, cfg)

    user_ind = get_user_ind(game, user["session_token"])
    game["users"][user_ind]["profit_per_sec"] = user_profit
    return game


def get_factory_profit(game, factory, cfg=None):
    """Получение профита фабрики"""

    if cfg is None:
        cfg = fetch_config()

    if factory["city_id"] is None or factory["source_id"] is None:
        return 0

    city = get_city(game, factory["city_id"])
    source = get_source(game, factory["source_id"])

    if source["remain"] <= 0:
        return 0

    fees = get_transfer_fee(city["coords"], factory["coords"], cfg) + get_transfer_fee(factory["coords"], source["coords"], cfg)
    products = cfg["max_products"][get_str_level_factory(factory)]
    level_dif = get_level_diff(factory, city, cfg)
    mult = get_profit_multi(level_dif, cfg)

    profit = get_city_payout(products, mult, cfg) - fees * products

    if profit <= 0:
        return 0
    return profit


def get_factory_deliver(city, factory, cfg=None):
    """Получить кол-во товаров которые берет город"""

    if cfg is None:
        cfg = fetch_config()

    products = cfg["max_products"][get_str_level_factory(factory)]
    level_dif = get_level_diff(factory, city, cfg)
    mult = get_profit_multi(level_dif, cfg)
    return mult * products
