import chess
import chess.pgn
import io
def get_moves(game):
    pgn = io.StringIO(game)
    game_pgn = chess.pgn.read_game(pgn)
    return game_pgn
