import chessdotcom
import datetime
client = chessdotcom.ChessDotComClient(user_agent="my python database")
def check_name(name):
    try:
        client.get_player_profile(name)
        return True
    except:
        print("failed")
        return False
def get_games(name):
    profile = client.get_player_profile(name)
    creation_date = datetime.datetime.fromtimestamp(profile.player.joined)
    player_games = []
    year = creation_date.year
    month = creation_date.month

    verschil = (datetime.datetime.now().year - year) *12 + datetime.datetime.now().month - month
    for i in range(verschil):
        month_games = (client.get_player_games_by_month(name,year,month).games)
        for game in month_games:
            player_games.append(game)
        month += 1
        if month > 12:
            month = 1
            year += 1
        print(year,month)
    print(len(player_games))
    return player_games