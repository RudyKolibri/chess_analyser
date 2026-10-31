from time import sleep

import math
import chessdotcom
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
aantal_threads = 5
client = chessdotcom.ChessDotComClient(user_agent="my python data analyser")
def check_name(name):
    try:
        client.get_player_profile(name)

        return True
    except Exception as e:
        print(f"failed : {e}")
        return False
def get_games_worker(name,year,month,aantal):
   worker_games = []
   for i in range(aantal):
        succeed = False
        pogingen = 0
        while not succeed and pogingen <3:
            try:
                month_games = (client.get_player_games_by_month(name, year, month).games)
                for game in month_games:
                    worker_games.append(game)
                succeed = True
            except: pogingen += 1
        month += 1
        if month > 12:
            year += 1
            month -=12
   return worker_games
def get_games(name):
    global player_games
    profile = client.get_player_profile(name)
    creation_date = datetime.datetime.fromtimestamp(profile.player.joined)
    player_games = []
    year = creation_date.year
    month = creation_date.month

    verschil = (datetime.datetime.now().year - year) *12 + datetime.datetime.now().month - month
    aantal_per_thread = verschil/aantal_threads
    with ThreadPoolExecutor(max_workers=aantal_threads) as executor:
        futures = []
        aantal_per_thread = math.ceil(aantal_per_thread)
        for i in range(aantal_threads):

            if (year >= datetime.datetime.now().year) and (month > datetime.datetime.now().month):
                break

            futures.append(executor.submit(get_games_worker, name, year, month, aantal_per_thread))
            month += aantal_per_thread
            while month > 12:
                year += 1
                month = month - 12
        for future in as_completed(futures):
            player_games.extend(future.result())
    print(len(player_games))
    return player_games