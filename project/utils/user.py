from datetime import datetime as dt
from project.utils.common import get_random_string


def new_user(username):
    """Создание игрового профиля"""
    data = {
        "username": username,
        "session_token": get_random_string(40),
        "is_ready": False,
        "balance": 350000,
        "profit_per_sec": 0,
        "datetime": dt.utcnow().isoformat()
    }
    return data
