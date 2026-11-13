# data.py
# Loads weekly NFL player stats from the free, public nflverse data project.

import io

import pandas as pd
import requests
import streamlit as st

DATA_URL = ("https://github.com/nflverse/nflverse-data/releases/download/"
            "stats_player/stats_player_week_{season}.csv")

SEASONS = [2026, 2025]
POSITIONS = ["QB", "RB", "WR", "TE"]

# Only the columns the app uses (keeps the download fast and memory small)
COLUMNS = [
    "player_id", "player_display_name", "position", "season", "week",
    "season_type", "team", "opponent_team",
    "completions", "attempts", "passing_yards", "passing_tds", "passing_interceptions",
    "carries", "rushing_yards", "rushing_tds",
    "receptions", "targets", "receiving_yards", "receiving_tds",
    "target_share", "air_yards_share", "fantasy_points_ppr",
]

# Friendly names for stat columns, shown in dropdowns and tables
STAT_LABELS = {
    "passing_yards": "Passing Yards",
    "passing_tds": "Passing TDs",
    "completions": "Completions",
    "attempts": "Pass Attempts",
    "passing_interceptions": "Interceptions",
    "rushing_yards": "Rushing Yards",
    "carries": "Rush Attempts",
    "rushing_tds": "Rushing TDs",
    "receiving_yards": "Receiving Yards",
    "receptions": "Receptions",
    "targets": "Targets",
    "receiving_tds": "Receiving TDs",
    "target_share": "Target Share",
    "air_yards_share": "Air Yards Share",
    "fantasy_points_ppr": "Fantasy Points (PPR)",
}

# Which stats make sense for each position
POSITION_STATS = {
    "QB": ["passing_yards", "passing_tds", "completions", "attempts",
           "passing_interceptions", "rushing_yards", "fantasy_points_ppr"],
    "RB": ["rushing_yards", "carries", "rushing_tds", "receptions",
           "receiving_yards", "targets", "fantasy_points_ppr"],
    "WR": ["receiving_yards", "receptions", "targets", "receiving_tds",
           "target_share", "air_yards_share", "fantasy_points_ppr"],
    "TE": ["receiving_yards", "receptions", "targets", "receiving_tds",
           "target_share", "air_yards_share", "fantasy_points_ppr"],
}

# Stats that are percentages (stored as decimals)
SHARE_STATS = {"target_share", "air_yards_share"}


@st.cache_data(ttl=60 * 60 * 6, show_spinner="Loading NFL stats...")
def load_weekly_stats(season):
    """Download one season of weekly player stats. Cached for 6 hours."""
    # requests brings its own up-to-date security certificates, which avoids
    # SSL certificate errors that some Mac Python installs run into
    response = requests.get(DATA_URL.format(season=season), timeout=60)
    response.raise_for_status()
    df = pd.read_csv(io.StringIO(response.text), usecols=COLUMNS, low_memory=False)
    df = df[df["position"].isin(POSITIONS)].copy()
    return df
