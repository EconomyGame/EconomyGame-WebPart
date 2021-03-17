from datetime import datetime as dt
from datetime import timedelta
from bson.objectid import ObjectId

from project.utils.mongo import fetch_config
from project.utils.resource import generate_resource_levels, generate_resource_stages


def generate_cities():
    """Создание городов для игровой сессии"""
    cfg = fetch_config()
    prepared_cities = list(zip(cfg["cities"]["cities_names"][:cfg["count_cities"]], cfg["map"]["cities"]))
    cities = [{
        "name": name,
        "coords": coords,
        "resource_levels": generate_resource_levels(cfg),
        "resource_stage": generate_resource_stages(cfg),
        "resource_delta": cfg["cities"]["requied_levels"]["level_1"],
        "datetime": dt.utcnow()
    } for name, coords in prepared_cities]
    return cities