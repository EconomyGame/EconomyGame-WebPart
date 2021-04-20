from datetime import datetime as dt

from project.utils.standart.mongo import fetch_config
from project.utils.objects.resource import generate_resource_levels, generate_resource_stages, generate_resource_deltas
from project.utils.standart.common import get_random_string


def generate_cities(cfg=None):
    """Создание городов для игровой сессии"""
    if cfg is None:
        cfg = fetch_config()

    prepared_cities = list(zip(cfg["cities"]["cities_names"][:cfg["count_cities"]], cfg["map"]["cities"]))
    cities = [{
        "_id": get_random_string(40),
        "name": name,
        "coords": coords,
        "resource_levels": generate_resource_levels(cfg),
        "resource_stage": generate_resource_stages(cfg),
        "resource_delta": generate_resource_deltas(cfg),
        "datetime": dt.utcnow().isoformat()
    } for name, coords in prepared_cities]
    return cities
