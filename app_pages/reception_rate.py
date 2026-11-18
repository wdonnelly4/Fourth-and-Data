# Reception Rate: how often targets turn into catches, and what each target is worth.

import streamlit as st

from common import (BLUE, PCT, ONE_DECIMAL, get_weekly, position_multiselect,
                    require_rows, team_select)
from metrics import reception_rate_table

st.title("Reception Rate")
st.write("Reception rate (catch rate) is receptions divided by targets. It's useful for "
         "reception props: a high catch rate plus steady targets usually means a reliable "
         "receptions floor. **Yards / Target** shows how much each target is actually worth.")

weekly = get_weekly()

col1, col2, col3 = st.columns(3)
with col1:
    positions = position_multiselect("rr_positions", default=["WR", "TE", "RB"])
with col2:
    team = team_select(weekly, key="rr_team")
with col3:
    min_targets = st.slider("Minimum targets", 1, 100, 25, key="rr_min_targets",
                            help="Filters out players with too few targets for a fair rate.")

table = reception_rate_table(weekly, positions, team, min_targets)
require_rows(table)
st.dataframe(table.drop(columns="player_id").head(100), hide_index=True,
             use_container_width=True,
             column_config={"Catch Rate %": PCT, "Yards / Target": ONE_DECIMAL,
                            "Yards / Reception": ONE_DECIMAL})

st.subheader("Volume vs. efficiency")
st.write("Each dot is a player. The best options combine lots of targets (right) with a "
         "high catch rate (top).")
st.scatter_chart(table, x="Targets", y="Catch Rate %", color=BLUE)
