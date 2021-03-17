import random
import string

from project.utils.mongo import fetch_game_by_id


def get_random_string(size=10):
    """Генерация рандомной строки из цифр и ascii символов длиной size"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(size))


def check_auth(request):
    """Проверка авторизации по request"""
    session_token = request.headers.get('Authorization')
    game_id = request.headers.get('Game')

    game = fetch_game_by_id(game_id)
    if game is not None and session_token in list(map(lambda x: x["session_token"], game["users"])):
        return game
    else:
        return
