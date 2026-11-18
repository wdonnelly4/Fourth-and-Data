# Leaderboard: top players at a position by per-game average.

import streamlit as st

from common import get_weekly
from data import POSITION_STATS, POSITIONS, SHARE_STATS, STAT_LABELS

st.title("Leaderboard")
st.write("Players ranked by their per-game average in the stat you choose.")

weekly = get_weekly()

left, middle, right = st.columns(3)
position = left.radio("Position", POSITIONS, horizontal=True, key="board_position")
stat = middle.selectbox("Rank by", POSITION_STATS[position],
                        format_func=lambda s: STAT_LABELS[s], key="board_stat")

df = weekly[weekly["position"] == position]
max_games = int(df.groupby("player_id")["week"].count().max())
min_games = right.slider("Minimum games played", 1, max_games, min(3, max_games))

board = (df.groupby("player_id")
           .agg(Player=("player_display_name", "last"),
                Team=("team", "last"),
                Games=("week", "count"),
                Average=(stat, "mean"))
           .query("Games >= @min_games")
           .sort_values("Average", ascending=False)
           .head(25)
           .reset_index(drop=True))
board.index = board.index + 1  # rank starts at 1

if stat in SHARE_STATS:
    board["Average"] = (board["Average"] * 100).round(1)
    board = board.rename(columns={"Average": f"{STAT_LABELS[stat]} (%) per game"})
else:
    board["Average"] = board["Average"].round(1)
    board = board.rename(columns={"Average": f"{STAT_LABELS[stat]} per game"})

st.dataframe(board, use_container_width=True)
