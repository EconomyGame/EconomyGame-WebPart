from datetime import datetime as dt

from project.utils.mongo import fetch_game_by_id
from project.utils.common import validate_coords


def make_factory(data):
    """Создание фабрики"""

    game = fetch_game_by_id(data["game_id"])
    if not validate_coords(game, data["coords"]):
        return dict(status=False, message="Coords error")

    data = {
        "session_token": data["session_token"],
        "resource_id": data["resource_id"],
        "coords": data["coords"],
        "city_name": None,
        "source_coords": None,
        "level": 1,
        "coef": 0.5,
        "datetime": dt.utcnow().isoformat()
    }

    return dict(status=True, factory=data)
