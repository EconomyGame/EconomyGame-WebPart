from datetime import datetime as dt
from project.utils.common import get_random_string


def new_user():
    """Создание игрового профиля"""
    data = {
        "session_token": get_random_string(20),
        "is_ready": False,
        "balance": 0,
        "profit_per_sec": 0,
        "datetime": dt.utcnow().isoformat()
    }
    return data
