# data.py
# Loads NFL data from the free, public nflverse project (github.com/nflverse).
# Every loader is cached for 6 hours so the app doesn't re-download on every click.

import io

import pandas as pd
import requests
import streamlit as st

BASE_URL = "https://github.com/nflverse/nflverse-data/releases/download"
CACHE_SECONDS = 60 * 60 * 6

SEASONS = [2026, 2025]
POSITIONS = ["QB", "RB", "WR", "TE"]

# ---------- Weekly player stats ----------

WEEKLY_COLUMNS = [
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

# Stats stored as decimals (0.27 = 27%)
SHARE_STATS = {"target_share", "air_yards_share"}

# ---------- Play-by-play (used starting in Phase 2) ----------

# A starter set of play-by-play columns. Each page passes only the columns it needs.
PBP_BASE_COLUMNS = [
    "game_id", "season", "week", "season_type", "posteam", "defteam",
    "play_type", "down", "ydstogo", "yardline_100", "drive",
    "passer_player_id", "passer_player_name",
    "receiver_player_id", "receiver_player_name",
    "rusher_player_id", "rusher_player_name",
    "yards_gained", "epa", "success",
]


# ---------- Download helpers ----------

def _download(path):
    """Download one nflverse release file and return its raw bytes."""
    response = requests.get(f"{BASE_URL}/{path}", timeout=120)
    response.raise_for_status()
    return response.content


def _read_release(name, columns=None, csv_ext=".csv"):
    """Read an nflverse file as Parquet (fast). Falls back to CSV if pyarrow isn't installed."""
    try:
        return pd.read_parquet(io.BytesIO(_download(name + ".parquet")), columns=columns)
    except ImportError:
        compression = "gzip" if csv_ext.endswith(".gz") else None
        return pd.read_csv(io.BytesIO(_download(name + csv_ext)), usecols=columns,
                           compression=compression, low_memory=False)


# ---------- Cached loaders ----------

@st.cache_data(ttl=CACHE_SECONDS, show_spinner="Loading weekly player stats...")
def load_weekly_stats(season):
    df = _read_release(f"stats_player/stats_player_week_{season}", columns=WEEKLY_COLUMNS)
    return df[df["position"].isin(POSITIONS)].copy()


@st.cache_data(ttl=CACHE_SECONDS, show_spinner="Loading snap counts...")
def load_snap_counts(season):
    df = _read_release(f"snap_counts/snap_counts_{season}")
    df["position"] = df["position"].replace({"HB": "RB"})  # nflverse uses both labels
    return df[df["position"].isin(POSITIONS) & (df["offense_snaps"] > 0)].copy()


@st.cache_data(ttl=CACHE_SECONDS, show_spinner="Loading the schedule...")
def load_schedule():
    """Every NFL game since 1999, including closing betting lines."""
    return _read_release("schedules/games")


@st.cache_data(ttl=CACHE_SECONDS, show_spinner="Loading play-by-play data...")
def load_pbp(season, columns=tuple(PBP_BASE_COLUMNS)):
    """One season of play-by-play. Pass a tuple of only the columns you need."""
    return _read_release(f"pbp/play_by_play_{season}", columns=list(columns), csv_ext=".csv.gz")
