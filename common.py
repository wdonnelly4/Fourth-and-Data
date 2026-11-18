# common.py
# Shared pieces every page uses: the sidebar filters, safe data loading, and widgets.

import streamlit as st

import data
from metrics import regular_season_only

BLUE = "#2a78d6"    # main chart color
ORANGE = "#eb6834"  # second color (blue/orange stays readable for colorblind users)

# Column formats for tables that store percentages as 0-100
PCT = st.column_config.NumberColumn(format="%.1f%%")
ONE_DECIMAL = st.column_config.NumberColumn(format="%.1f")
TREND = st.column_config.NumberColumn(format="%+.1f",
                                      help="Last 3 games minus season average")


def show_sidebar_filters():
    """Filters shared by every page. Their values live in st.session_state."""
    st.sidebar.selectbox("Season", data.SEASONS, key="season",
                         help="2026 updates during the season as new games are played.")
    st.sidebar.checkbox("Include playoff games", key="include_playoffs")
    st.sidebar.caption("Data: nflverse (free public NFL data), refreshed every 6 hours.")
    st.sidebar.caption("For research and entertainment only. This app does not place bets.")


def season():
    return st.session_state.get("season", data.SEASONS[0])


def _load_or_stop(loader, *args):
    """Run a data loader; if it fails, show a friendly error and stop the page."""
    try:
        return loader(*args)
    except Exception as error:
        st.error("Couldn't load NFL data right now. Check your internet connection and try again.")
        st.caption(f"Technical details: {type(error).__name__}: {error}")
        st.stop()


def get_weekly():
    df = _load_or_stop(data.load_weekly_stats, season())
    return regular_season_only(df, st.session_state.get("include_playoffs", False))


def get_snaps():
    # nflverse snap counts include playoffs under game_type
    df = _load_or_stop(data.load_snap_counts, season())
    if not st.session_state.get("include_playoffs", False):
        df = df[df["game_type"] == "REG"]
    return df


def get_schedule():
    return _load_or_stop(data.load_schedule)


def team_select(df, key, column="team", label="Team"):
    """Dropdown of teams with an 'All teams' option. Returns None for all teams."""
    teams = sorted(df[column].dropna().unique())
    choice = st.selectbox(label, ["All teams"] + teams, key=key)
    return None if choice == "All teams" else choice


def position_multiselect(key, default):
    positions = st.multiselect("Positions", data.POSITIONS, default=default, key=key)
    if not positions:
        st.info("Choose at least one position.")
        st.stop()
    return positions


def require_rows(table):
    """Stop the page with a message if the filters leave nothing to show."""
    if table.empty:
        st.warning("No players match these filters. Try lowering the minimum or choosing all teams.")
        st.stop()


def choose_player(weekly, key):
    """Position radio + player dropdown (best fantasy scorers first). Returns a Player."""
    from player import Player

    position = st.radio("Position", data.POSITIONS, horizontal=True, key=f"{key}_position")
    df = weekly[weekly["position"] == position]
    if df.empty:
        st.warning("No games found for these filters yet.")
        st.stop()

    players = (df.groupby("player_id")
                 .agg(name=("player_display_name", "last"), team=("team", "last"),
                      points=("fantasy_points_ppr", "sum"))
                 .sort_values("points", ascending=False))
    player_id = st.selectbox(
        "Choose a player", players.index, key=f"{key}_player",
        format_func=lambda pid: f"{players.loc[pid, 'name']} ({players.loc[pid, 'team']})",
        help="Listed by total fantasy points, best first. Start typing to search.",
    )
    return Player(df[df["player_id"] == player_id])
