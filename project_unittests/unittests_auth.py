import requests
import unittest

"""
Документацию по API вы можете найти здесь:
http://tp-project2021.herokuapp.com/api/v1/docs/
"""

api_create_game = "https://tp-project2021.herokuapp.com/api/v1/game_lobby/create_game"
api_fetch_game = "https://tp-project2021.herokuapp.com/api/v1/game_lobby/fetch_game"


def get_session():
    """Получение game_id и session_token в которых будем тестировать Авторизацию"""
    _request = requests.post(api_create_game)
    assert _request.status_code == 200

    game = _request.json()["game"]
    user = _request.json()["user"]
    return game, user


class TestAuth(unittest.TestCase):
    """
    Тестирование проходит на сервере, от которого мы ожидаем корректный ответ

    Для этого мы используем API-документацию
    """

    def test_without_auth(self):
        """Проверка без авторизации"""
        _request = requests.get(api_fetch_game)
        self.assertEqual(_request.status_code, 401)

    def test_without_game_id(self):
        game, user = get_session()
        _request = requests.get(api_fetch_game, headers={"Authorization": user["session_token"]})
        self.assertEqual(_request.status_code, 401)

    def test_without_user(self):
        game, user = get_session()
        _request = requests.get(api_fetch_game, headers={"Game": game["_id"]})
        self.assertEqual(_request.status_code, 401)

    def test_user_ready(self):
        game, user = get_session()
        _request = requests.get(api_fetch_game, headers={"Game": game["_id"],
                                                         "Authorization": user["session_token"]})
        self.assertEqual(_request.status_code, 200)
