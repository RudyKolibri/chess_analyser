
import streamlit
import sqlite3
from chesscom import check_name, get_games
from main import save_games
import pandas as pd

streamlit.title("Chess analyser and database")
streamlit.header("games")
conn = sqlite3.connect('chess_analyser.db')
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS games (white TEXT, black TEXT, white_elo INTEGER, black_elo INTEGER, game_result TEXT, pgn TEXT)")
df = pd.read_sql_query("SELECT * FROM games", conn)
username = streamlit.sidebar.text_input("Enter your username")
if username:
    if check_name(username):
        streamlit.sidebar.header(f"hello {username}")
        with streamlit.sidebar.spinner("loading games"):
            games = get_games(username)
            save_games(games)
        streamlit.sidebar.header("games loaded")
    else:
        streamlit.sidebar.error("username not found")
if not df.empty:
    streamlit.success("games loaded")
    for index, row in df.iterrows():
        is_white = row["white"]
        is_black = row["black"]
        white_elo = row["white_elo"]
        black_elo = row["black_elo"]
        game_result = row["game_result"]

        is_user_white = username.lower() == is_white.lower() if username else True
        if game_result == "1-0":
            if is_user_white:
                status, bg_color, text_color = (
                    "1 - 0",
                    "#d1e7dd",
                    "#0f5132",
                )  # Groen
            else:
                status, bg_color, text_color = "1 - 0", "#f8d7da", "#842029"  # Rood
        elif game_result == "0-1":
            if not is_user_white:
                status, bg_color, text_color = (
                    "0 - 1",
                    "#d1e7dd",
                    "#0f5132",
                )  # Groen
            else:
                status, bg_color, text_color = "0 - 1", "#f8d7da", "#842029"  # Rood
        elif game_result in ["1/2-1/2", "Drawn"]:
            status, bg_color, text_color = "1/2 - 1/2", "#cfe2ff", "#084298"  # Blauw
        else:
            status, bg_color, text_color = (
                game_result,
                "#e2e3e5",
                "#383d41",
            )  # Grijs (fallback)

        badge_html = f"""
                <div style="background-color: {bg_color}; color: {text_color}; 
                            padding: 6px 12px; border-radius: 8px; text-align: center; 
                            font-weight: bold; font-size: 13px; float: right;">
                    {status}
                </div>
                """
        with streamlit.container(border=True):
            col_left, col_right = streamlit.columns([3, 1])
            with col_left:
                streamlit.markdown(f"{is_white}[{white_elo}] vs {is_black}[{black_elo}]")
            with col_right:
                streamlit.markdown(badge_html,unsafe_allow_html=True)
if df.empty:
    streamlit.text("No games found, enter a username in the sidebar")

