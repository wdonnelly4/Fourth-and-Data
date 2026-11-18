# Prop Analyzer: how often a player has gone over a prop line.

import math

import pandas as pd
import streamlit as st

from common import BLUE, ORANGE, choose_player, get_weekly
from data import POSITION_STATS, SHARE_STATS, STAT_LABELS

st.title("Prop Analyzer")
st.write("Pick a player and a stat, enter a prop line, and see how often they've gone over it.")

player = choose_player(get_weekly(), key="prop")

# Fantasy points and share stats aren't sportsbook props
prop_stats = [s for s in POSITION_STATS[player.position]
              if s not in SHARE_STATS and s != "fantasy_points_ppr"]

left, middle, right = st.columns(3)
stat = left.selectbox("Stat", prop_stats, format_func=lambda s: STAT_LABELS[s])

# Default line: the player's average rounded to the nearest .5 below it
default_line = max(math.floor(player.average(stat)) + 0.5, 0.5)
line = middle.number_input("Prop line", min_value=0.0, value=default_line, step=0.5,
                           key=f"line_{player.player_id}_{stat}")

games = player.games_played()
if games > 1:
    last_n = right.slider("Last N games", min_value=1, max_value=games, value=min(10, games))
else:
    last_n = 1
    right.caption("Only 1 game played so far.")

result = player.hit_rate(stat, line, last_n)

cols = st.columns(4)
cols[0].metric("Over", result["overs"])
cols[1].metric("Under", result["unders"])
cols[2].metric("Push", result["pushes"])
cols[3].metric("Over rate", f"{result['over_rate']:.0%}")

recent = player.recent_games(last_n)
average = recent[stat].fillna(0).mean()
st.write(f"Over his last **{result['games']}** games, {player.name} went **over "
         f"{line:g} {STAT_LABELS[stat].lower()}** in **{result['overs']}** of them and "
         f"averaged **{average:.1f}**.")

# Each game is blue if it went over the line, orange if under
values = recent[stat].fillna(0)
chart = pd.DataFrame({"Week": recent["week"],
                      "Over": values.where(values > line, 0),
                      "Under": values.where(values <= line, 0)})
st.bar_chart(chart, x="Week", y=["Over", "Under"], color=[BLUE, ORANGE])
st.caption(f"Prop line: {line:g}. Past results don't guarantee future outcomes. "
           "This tool is for research only and does not place bets.")
