# Schedule & Lines: every game with results and closing betting lines.

import streamlit as st

from common import get_schedule, season
from metrics import schedule_table

st.title("Schedule & Lines")
st.write("Every game this season with the final score and the closing betting lines. "
         "**Favorite** shows which team was favored and by how many points.")

games = get_schedule()
season_games = games[games["season"] == season()]

if season_games.empty:
    st.warning("No schedule found for this season yet.")
    st.stop()

col1, col2 = st.columns(2)
teams = sorted(set(season_games["home_team"]) | set(season_games["away_team"]))
team = col1.selectbox("Team", ["All teams"] + teams, key="sch_team")
weeks = sorted(season_games["week"].unique())
week = col2.selectbox("Week", ["All weeks"] + weeks, key="sch_week")

table = schedule_table(games, season(),
                       team=None if team == "All teams" else team,
                       week=None if week == "All weeks" else week)

st.dataframe(table, hide_index=True, use_container_width=True,
             column_config={"Total": st.column_config.NumberColumn(format="%.1f"),
                            "Away ML": st.column_config.NumberColumn(format="%+d"),
                            "Home ML": st.column_config.NumberColumn(format="%+d")})
st.caption("Lines are closing lines from nflverse. Moneyline: -150 means bet $150 to win $100; "
           "+130 means bet $100 to win $130.")
