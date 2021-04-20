import time
import threading

from project.app import app, mongo
from project.utils.standart.mongo import get_active_games, update_game

waiting_time = 2


def worker_job():
    games = get_active_games()
    for i in games:
        for j in i["users"]:
            j["balance"] += j["profit_per_sec"] * waiting_time
        for j in i["sources"]:
            j["remain"] -= j["delta"] * waiting_time
        for j in i["cities"]:
            for k in j["resource_delta"]:
                j["resource_stage"][k] += j["resource_delta"][k] * waiting_time
        update_game(str(i["_id"]), i)
    print("worker job current time : {}".format(time.time()))


if __name__ == "__main__":
    while True:
        threading.Thread(target=worker_job, args=()).start()
        time.sleep(2)

