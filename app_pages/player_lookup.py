# Player Lookup: one player's averages, weekly fantasy points, and game log.

import streamlit as st

from common import BLUE, choose_player, get_weekly
from data import POSITION_STATS, SHARE_STATS, STAT_LABELS

st.title("Player Lookup")
st.write("Choose a position and player to see their averages, weekly fantasy points, and full game log.")

player = choose_player(get_weekly(), key="lookup")


def format_value(stat, value):
    return f"{value:.1%}" if stat in SHARE_STATS else f"{value:.1f}"


st.subheader(f"{player.name} ({player.team}, {player.position})")
stats = POSITION_STATS[player.position]
cols = st.columns(4)
cols[0].metric("Games", player.games_played())
cols[1].metric("PPR Points / Game", f"{player.average('fantasy_points_ppr'):.1f}")
cols[2].metric(f"{STAT_LABELS[stats[0]]} / Game", format_value(stats[0], player.average(stats[0])))
cols[3].metric(f"{STAT_LABELS[stats[1]]} / Game", format_value(stats[1], player.average(stats[1])))

st.markdown("**Fantasy points by week (PPR)**")
chart = player.games[["week", "fantasy_points_ppr"]].rename(
    columns={"week": "Week", "fantasy_points_ppr": "PPR Points"})
st.line_chart(chart, x="Week", y="PPR Points", color=BLUE)

st.markdown("**Game log**")
log = player.games[["week", "opponent_team"] + stats].copy()
for stat in SHARE_STATS & set(stats):
    log[stat] = (log[stat] * 100).round(1)
log = log.rename(columns={"week": "Week", "opponent_team": "Opponent"})
log = log.rename(columns={s: STAT_LABELS[s] + (" (%)" if s in SHARE_STATS else "") for s in stats})
st.dataframe(log, hide_index=True, use_container_width=True)
