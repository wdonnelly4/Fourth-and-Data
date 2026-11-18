# Snap Shares: the percent of offensive plays each player was on the field for.

import streamlit as st

from common import (PCT, get_snaps, position_multiselect, require_rows, team_select)
from metrics import snap_share_table, team_snap_grid

st.title("Snap Shares")
st.write("Snap share is the percent of a team's offensive plays a player was on the field. "
         "A player can't produce if he isn't playing, so snap share is the first thing to "
         "check when a role is changing, like after an injury or a trade.")

snaps = get_snaps()

col1, col2, col3 = st.columns(3)
with col1:
    positions = position_multiselect("ss_positions", default=["RB", "WR", "TE"])
with col2:
    team = team_select(snaps, key="ss_team")
with col3:
    min_games = st.slider("Minimum games", 1, int(snaps["week"].nunique()), 3, key="ss_min_games")

table = snap_share_table(snaps, positions, team, min_games)
require_rows(table)
st.dataframe(table.drop(columns="pfr_player_id").head(100), hide_index=True,
             use_container_width=True,
             column_config={"Snap Share %": PCT, "Last Game %": PCT})

st.subheader("Team snap share by week")
st.write("See how a team splits snaps at each position week by week.")
grid_team = st.selectbox("Team", sorted(snaps["team"].unique()), key="ss_grid_team")
grid = team_snap_grid(snaps, grid_team, positions)
st.dataframe(grid, hide_index=True, use_container_width=True,
             column_config={c: PCT for c in grid.columns if c not in ("Player", "Pos")})
