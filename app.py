# app.py
# Fourth & Data: NFL analytics for fantasy football and player props.
# This file sets up navigation; each page lives in the app_pages folder.

import streamlit as st

from common import show_sidebar_filters

st.set_page_config(page_title="Fourth & Data", layout="wide")

pages = {
    "Overview": [
        st.Page("app_pages/home.py", title="Home", default=True),
    ],
    "Player Tools": [
        st.Page("app_pages/player_lookup.py", title="Player Lookup"),
        st.Page("app_pages/prop_analyzer.py", title="Prop Analyzer"),
        st.Page("app_pages/leaderboard.py", title="Leaderboard"),
    ],
    "Usage & Volume": [
        st.Page("app_pages/target_shares.py", title="Target Shares"),
        st.Page("app_pages/snap_shares.py", title="Snap Shares"),
        st.Page("app_pages/reception_rate.py", title="Reception Rate"),
        st.Page("app_pages/carries.py", title="Carries"),
    ],
    "League": [
        st.Page("app_pages/schedule.py", title="Schedule & Lines"),
    ],
}

navigation = st.navigation(pages)
show_sidebar_filters()
navigation.run()
