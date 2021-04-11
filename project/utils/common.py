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


def validate_coords(game, coords):
    if game is None:
        return False

    used = [x["coords"] for x in game["cities"]] + \
           [x["coords"] for x in game["sources"]] + \
           [x["coords"] for x in game["factories"]]
    return list(coords) not in used


def get_user_ind(game, session_token):
    res_find = [x["session_token"] == session_token for x in game["users"]]
    try:
        return res_find.index(True)
    except ValueError as D:
        return -1


def get_factory_ind(game, factory_id):
    res_find = [x["_id"] == factory_id for x in game["factories"]]
    try:
        return res_find.index(True)
    except ValueError as D:
        return -1

