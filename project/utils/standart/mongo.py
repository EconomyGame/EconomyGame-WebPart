from bson.json_util import ObjectId
import datetime

from project.app import mongo


def fetch_game_by_id(game_id):
    """Поиск Game по _id"""
    return mongo.db.games.find_one({"_id": ObjectId(game_id)})


def fetch_game_by_code(ref_code):
    """Поиск игры по реф. коду"""
    return mongo.db.games.find_one({"ref_code": ref_code})


def insert_game(data):
    """Создание игры с назначенной data"""
    return mongo.db.games.insert_one(data).inserted_id


def update_game(game_id, data):
    """Обновление параметров игры"""
    return mongo.db.games.update_one({"_id": ObjectId(game_id)}, {"$set": data})


def fetch_config():
    """Получение актуального конфига игры"""
    return mongo.db.config.find_one({})


def get_active_games():
    return mongo.db.games.find({"is_started": True})
