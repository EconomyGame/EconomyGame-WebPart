from datetime import datetime as dt

from project.utils.mongo import fetch_config
from project.utils.common import get_random_string


def generate_sources(cfg=None):
    """Создание источников с ресурсами для игровой сессии"""
    if cfg is None:
        cfg = fetch_config()

    remain = (cfg["cities"]["upgrades_levels"]["level_1"] +
              cfg["cities"]["upgrades_levels"]["level_2"] +
              cfg["cities"]["upgrades_levels"]["level_3"] +
              cfg["cities"]["upgrades_levels"]["level_4"]) * cfg["count_cities"] // cfg["count_users"] * 2
    sources = [{
        "_id": get_random_string(40),
        "resource_id": x["resource_id"],
        "coords": x["coords"],
        "remain": remain,
        "delta": 0,
        "datetime": dt.utcnow()
    } for x in cfg["map"]["sources"]]
    return sources
