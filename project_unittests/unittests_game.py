import requests
import unittest

"""
Документацию по API вы можете найти здесь:
http://tp-project2021.herokuapp.com/api/v1/docs/
"""

api_create_game = "https://tp-project2021.herokuapp.com/api/v1/game_lobby/create_game"
api_fetch_game = "https://tp-project2021.herokuapp.com/api/v1/game_lobby/fetch_game"
api_join_game = "https://tp-project2021.herokuapp.com/api/v1/game_lobby/join_game"
api_leave_game = "https://tp-project2021.herokuapp.com/api/v1/game_lobby/leave_game"
api_update_ready = "https://tp-project2021.herokuapp.com/api/v1/game_lobby/update_ready"
api_start_game = "https://tp-project2021.herokuapp.com/api/v1/game_lobby/start_game"


def get_session():
    """Получение game_id и session_token в которых будем тестировать Авторизацию

    Функция заранее протестирована в TestGame #1 и успешно работает.
    Дубликат теста лежит в классе.
    """
    _request = requests.post(api_create_game)
    assert _request.status_code == 200

    game = _request.json()["game"]
    user = _request.json()["user"]
    return game, user


class TestGame(unittest.TestCase):
    """
    Тестирование проходит на сервере, от которого мы ожидаем корректный ответ

    Для этого мы используем API-документацию
    """

    def test_create_game(self):
        """Проверка создания игры"""
        _request = requests.post(api_create_game)
        self.assertEqual(_request.status_code, 200)
        self.assertEqual(_request.json()["status"], True)

    def test_wrong_join_without_ref_code(self):
        _request = requests.get(api_join_game)
        self.assertEqual(_request.json()["status"], False)

    def test_wrong_join_with_ref_code(self):
        _request = requests.get(api_join_game, params={"ref_code": "unittests"})
        self.assertEqual(_request.json()["status"], False)

    def test_correct_join_with_ref_code(self):
        game = get_session()[0]
        _request = requests.get(api_join_game, params={"ref_code": game["ref_code"]})
        self.assertEqual(_request.json()["status"], True)
        self.assertEqual(_request.json()["game"]["_id"], game["_id"])

    def test_fetch_game(self):
        game, user = get_session()
        headers = {"Game": game["_id"], "Authorization": user["session_token"]}
        _request = requests.get(api_fetch_game, headers=headers)
        self.assertEqual(_request.json()["status"], True)

    def test_create_and_leave(self):
        game, user = get_session()
        headers = {"Game": game["_id"], "Authorization": user["session_token"]}
        _request = requests.get(api_leave_game, headers=headers)
        self.assertEqual(_request.json()["status"], True)
        self.assertEqual(_request.json()["game"]["users"], [])

    def test_create_join_and_leave(self):
        game, user = get_session()
        _request = requests.get(api_join_game, params={"ref_code": game["ref_code"]})
        self.assertEqual(_request.json()["status"], True)
        headers = {"Game": game["_id"], "Authorization": _request.json()["user"]["session_token"]}
        _request = requests.get(api_leave_game, headers=headers)
        self.assertEqual(_request.json()["status"], True)
        self.assertEqual(_request.json()["game"], game)

    def test_join_limit(self):
        game = get_session()[0]
        params = {"ref_code": game["ref_code"]}

        _request = requests.get(api_join_game, params=params)
        self.assertEqual(_request.json()["status"], True)
        self.assertEqual(_request.json()["game"]["_id"], game["_id"])

        _request = requests.get(api_join_game, params=params)
        self.assertEqual(_request.json()["status"], True)
        self.assertEqual(_request.json()["game"]["_id"], game["_id"])

        _request = requests.get(api_join_game, params=params)
        self.assertEqual(_request.json()["status"], True)
        self.assertEqual(_request.json()["game"]["_id"], game["_id"])

        _request = requests.get(api_join_game, params=params)
        self.assertEqual(_request.json()["status"], False)

    def test_update_ready(self):
        game, user = get_session()
        self.assertEqual(user["is_ready"], False)

        headers = {"Game": game["_id"], "Authorization": user["session_token"]}
        _request = requests.get(api_update_ready, headers=headers)
        self.assertEqual(_request.json()["user"]["is_ready"], True)

        _request = requests.get(api_update_ready, headers=headers)
        self.assertEqual(_request.json()["user"]["is_ready"], False)

    def test_start_game(self):
        game, user = get_session()
        self.assertEqual(user["is_ready"], False)

        headers = {"Game": game["_id"], "Authorization": user["session_token"]}
        _request = requests.get(api_update_ready, headers=headers)
        self.assertEqual(_request.json()["user"]["is_ready"], True)

        _request = requests.get(api_start_game, headers=headers)
        self.assertEqual(_request.json()["status"], True)
        self.assertEqual(_request.json()["game"]["is_started"], True)
