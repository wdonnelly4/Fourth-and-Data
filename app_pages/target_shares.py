# Target Shares: the percent of a team's targets that go to each player.

import streamlit as st

from common import (BLUE, ONE_DECIMAL, PCT, TREND, get_weekly, position_multiselect,
                    require_rows, team_select)
from metrics import target_share_table, weekly_trend

st.title("Target Shares")
st.write("Target share is the percent of a team's pass targets that go to a player. "
         "It's one of the most predictive stats for receiving yards and fantasy points, "
         "because volume tends to stay steady from week to week. **Trend** compares a "
         "player's last 3 games to his season average.")

weekly = get_weekly()

col1, col2, col3 = st.columns(3)
with col1:
    positions = position_multiselect("ts_positions", default=["WR", "TE", "RB"])
with col2:
    team = team_select(weekly, key="ts_team")
with col3:
    min_games = st.slider("Minimum games", 1, int(weekly["week"].nunique()), 3, key="ts_min_games")

table = target_share_table(weekly, positions, team, min_games)
require_rows(table)

st.dataframe(
    table.drop(columns="player_id").head(100),
    hide_index=True, use_container_width=True,
    column_config={"Target Share %": PCT, "Last 3 Games %": PCT, "Air Yards Share %": PCT,
                   "Targets / Game": ONE_DECIMAL, "Trend": TREND},
)

st.subheader("Weekly target share")
names = dict(zip(table["player_id"], table["Player"] + " (" + table["Team"] + ")"))
player_id = st.selectbox("Player", list(names), format_func=names.get, key="ts_player")
trend = weekly_trend(weekly, player_id, "target_share", as_percent=True)
st.line_chart(trend.rename(columns={"Value": "Target Share %"}),
              x="Week", y="Target Share %", color=BLUE)
