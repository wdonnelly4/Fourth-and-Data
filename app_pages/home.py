# Home page: what the app does and how to use it.

import streamlit as st

from common import get_weekly, season

st.title("Fourth & Data: NFL Analytics for Fantasy and Betting")
st.write("Real, weekly NFL data turned into the usage and efficiency stats that "
         "actually predict fantasy points and player props. Pick a page from the "
         "menu on the left, and use the Season filter to switch years.")

weekly = get_weekly()
latest_week = int(weekly["week"].max()) if not weekly.empty else 0
st.caption(f"{season()} season data through Week {latest_week}.")

st.subheader("What's inside")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Player Tools**")
    st.markdown("- **Player Lookup:** game logs and weekly fantasy points\n"
                "- **Prop Analyzer:** how often a player clears a prop line\n"
                "- **Leaderboard:** top players in any stat")
with col2:
    st.markdown("**Usage & Volume**")
    st.markdown("- **Target Shares:** who gets the looks, and who's trending up\n"
                "- **Snap Shares:** who's on the field\n"
                "- **Reception Rate:** catch rate and yards per target\n"
                "- **Carries:** rushing volume and backfield splits")
with col3:
    st.markdown("**League**")
    st.markdown("- **Schedule & Lines:** every game with the spread, total, and moneylines")

st.info("Why usage stats? Opportunity (targets, snaps, carries) is more stable from week "
        "to week than touchdowns or big plays, so it's one of the best predictors of "
        "future production.")
