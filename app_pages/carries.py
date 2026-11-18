# Carries: rushing volume, carry share, and backfield splits.

import streamlit as st

from common import (ONE_DECIMAL, PCT, get_weekly, position_multiselect, require_rows,
                    team_select)
from metrics import carries_table, team_carries_grid

st.title("Carries")
st.write("Carries are the clearest measure of a running back's workload. **Carry Share** "
         "is the percent of his team's rushing attempts he handled in the games he played, "
         "which shows who really leads a backfield.")

weekly = get_weekly()

col1, col2, col3 = st.columns(3)
with col1:
    positions = position_multiselect("ca_positions", default=["RB"])
with col2:
    team = team_select(weekly, key="ca_team")
with col3:
    min_games = st.slider("Minimum games", 1, int(weekly["week"].nunique()), 3, key="ca_min_games")

table = carries_table(weekly, positions, team, min_games)
require_rows(table)
st.dataframe(table.drop(columns="player_id").head(100), hide_index=True,
             use_container_width=True,
             column_config={"Carry Share %": PCT, "Carries / Game": ONE_DECIMAL,
                            "Yards / Carry": ONE_DECIMAL})

st.subheader("Backfield carries by week")
grid_team = st.selectbox("Team", sorted(weekly["team"].dropna().unique()), key="ca_grid_team")
st.dataframe(team_carries_grid(weekly, grid_team), hide_index=True, use_container_width=True)
