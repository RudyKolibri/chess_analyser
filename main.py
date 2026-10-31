from chesscom import *
from game import *
import sqlite3

database = sqlite3.connect('chess_analyser.db')
cursor = database.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS games (white TEXT, black TEXT, white_elo INTEGER, black_elo INTEGER, pgn TEXT)")
database.commit()

def save_games(games):
    for game in games:
        gamepgn = get_moves(game.pgn)
        exporter = chess.pgn.StringExporter(headers=False, variations=False, comments=False)
        plain_moves = gamepgn.accept(exporter)
        cursor.execute("INSERT INTO games (white, black, white_elo, black_elo, pgn) VALUES (?, ?, ?,?, ?)", (gamepgn.headers["White"], gamepgn.headers["Black"], gamepgn.headers["WhiteElo"], gamepgn.headers["BlackElo"], str(plain_moves)))
    database.commit()
    database.close()
def start():
    print("Welcome to chess_analyser.")

    valid_name =False
    while valid_name == False:
        name = input("Please enter your name: ")
        valid_name = check_name(name)
    games = get_games(name)
    save_games(games)
if __name__ == "__main__":
    start()