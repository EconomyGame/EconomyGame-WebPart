import requests
import unittest

api_create_game = "https://tp-project2021.herokuapp.com/api/v1/game_lobby/create_game"
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


def start_game():
    game, user = get_session()
    headers = {"Game": game["_id"], "Authorization": user["session_token"]}
    requests.get(api_update_ready, headers=headers)
    _request = requests.get(api_start_game, headers=headers)
    return _request.json()["game"], _request.status_code


class TestGame(unittest.TestCase):
    def test_generate_cities(self):
        game, status = start_game()
        self.assertEqual(200, status)
        self.assertIn("cities", game)
        for i in game["cities"]:
            self.assertIn("datetime", i)
            self.assertIn("name", i)
            self.assertIn("resource_delta", i)
            self.assertIn("resource_levels", i)
            self.assertIn("resource_stage", i)
            self.assertIn("coords", i)

    def test_generate_sources(self):
        game, status = start_game()
        self.assertEqual(200, status)
        self.assertIn("sources", game)
        for i in game["sources"]:
            self.assertIn("datetime", i)
            self.assertIn("coords", i)
            self.assertIn("remain", i)
            self.assertIn("delta", i)
            self.assertIn("resource_id", i)
