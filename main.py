from chess import pgn

from chesscom import *
from game import *
import sqlite3

def save_games(games):
    database = sqlite3.connect('chess_analyser.db')
    cursor = database.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS games (white TEXT, black TEXT, white_elo INTEGER, black_elo INTEGER, game_result TEXT, pgn TEXT)")
    database.commit()
    for game in games:
        gamepgn = get_moves(game.pgn)
        exporter = chess.pgn.StringExporter(headers=False, variations=False, comments=False)
        plain_moves = gamepgn.accept(exporter)
        cursor.execute("INSERT INTO games (white, black, white_elo, black_elo,game_result, pgn) VALUES (?, ?, ?,?,?, ?)", (gamepgn.headers["White"], gamepgn.headers["Black"], gamepgn.headers["WhiteElo"], gamepgn.headers["BlackElo"],gamepgn.headers["Result"], str(plain_moves)))
    database.commit()
    database.close()
def start(name):
    print("Welcome to chess_analyser.")
    print("start via consol : streamlit run app.py")
if __name__ == "__main__":
    start()