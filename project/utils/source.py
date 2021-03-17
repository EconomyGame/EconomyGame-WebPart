from datetime import datetime as dt
from datetime import timedelta
from bson.objectid import ObjectId

from project.utils.mongo import fetch_config
from project.utils.resource import generate_resource_levels, generate_resource_stages


def generate_sources():
    """Создание источников с ресурсами для игровой сессии"""
    cfg = fetch_config()
    sources = []
    return sources
