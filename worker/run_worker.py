import time
import threading

from project.app import app, mongo
from project.utils.standart.mongo import get_active_games, update_game, fetch_config
from project.utils.standart.update_profits import update_source, update_city
from project.sockets import broadcast_game

waiting_time = 3


def worker_job():
    cfg = fetch_config()
    games = get_active_games()
    is_updated = False
    for i in games:
        print("Opened #" + str(i["_id"]) + " | current time: {}".format(time.time()))
        for j in i["users"]:
            j["balance"] += j["profit_per_sec"] * waiting_time
        for j in i["sources"]:
            j["remain"] -= j["delta"] * waiting_time
            if j["remain"] < 0:
                is_updated = True
                j["remain"] = 0
                i = update_source(i, j, cfg)

        for j in i["cities"]:
            for k in j["resource_delta"]:
                j["resource_stage"][k] += j["resource_delta"][k] * waiting_time
                if j["resource_stage"][k] <= cfg["cities"]["upgrades_levels"]["level_" + str(j["resource_levels"][k])]:
                    is_updated = True
                    j["resource_stage"][k] = 0
                    j["resource_levels"][k] += 1
                    i = update_city(i, j, cfg)

        update_game(str(i["_id"]), i)
        if is_updated:
            broadcast_game(i)
        print("Closed #" + str(i["_id"]) + " | current time: {}".format(time.time()))


if __name__ == "__main__":
    while True:
        threading.Thread(target=worker_job, args=()).start()
        time.sleep(waiting_time)

