# app.py
# Fourth & Data: NFL analytics for fantasy football and player props.

import math

import pandas as pd
import streamlit as st

from data import (POSITION_STATS, POSITIONS, SEASONS, SHARE_STATS, STAT_LABELS,
                  load_weekly_stats)
from player import Player

st.set_page_config(page_title="Fourth & Data", layout="wide")

OVER_COLOR = "#3ffd00"   # green
UNDER_COLOR = "#eb3434"  # orange 


# ---------- Helpers ----------

def label(stat):
    return STAT_LABELS.get(stat, stat)


def format_value(stat, value):
    """Show shares as percentages and everything else with one decimal."""
    if stat in SHARE_STATS:
        return f"{value:.1%}"
    return f"{value:.1f}"


def build_player_list(df):
    """One entry per player, sorted by total fantasy points so the best players come first."""
    totals = (df.groupby("player_id")
                .agg(name=("player_display_name", "last"),
                     team=("team", "last"),
                     points=("fantasy_points_ppr", "sum"))
                .sort_values("points", ascending=False))
    return totals


def game_log_table(player):
    """The player's week-by-week stats with readable column names."""
    stats = POSITION_STATS[player.position]
    table = player.games[["week", "opponent_team"] + stats].copy()
    for stat in SHARE_STATS & set(stats):
        table[stat] = (table[stat] * 100).round(1)
    table = table.rename(columns={"week": "Week", "opponent_team": "Opponent"})
    table = table.rename(columns={s: label(s) + (" (%)" if s in SHARE_STATS else "")
                                  for s in stats})
    return table


# ---------- Sections ----------

def show_sidebar():
    st.sidebar.header("Filters")
    season = st.sidebar.selectbox("Season", SEASONS,
                                  help="2026 updates during the season as new games are played.")
    position = st.sidebar.radio("Position", POSITIONS, horizontal=True)
    include_playoffs = st.sidebar.checkbox("Include playoff games", value=False)
    st.sidebar.caption("Data: nflverse (free public NFL data), refreshed every 6 hours.")
    return season, position, include_playoffs


def show_player_lookup(player):
    st.subheader(f"{player.name} ({player.team}, {player.position})")

    stats = POSITION_STATS[player.position]
    cols = st.columns(4)
    cols[0].metric("Games", player.games_played())
    cols[1].metric("PPR Points / Game", f"{player.average('fantasy_points_ppr'):.1f}")
    cols[2].metric(f"{label(stats[0])} / Game", format_value(stats[0], player.average(stats[0])))
    cols[3].metric(f"{label(stats[1])} / Game", format_value(stats[1], player.average(stats[1])))

    st.markdown("**Fantasy points by week (PPR)**")
    chart = player.games[["week", "fantasy_points_ppr"]].rename(
        columns={"week": "Week", "fantasy_points_ppr": "PPR Points"})
    st.line_chart(chart, x="Week", y="PPR Points", color=OVER_COLOR)

    st.markdown("**Game log**")
    st.dataframe(game_log_table(player), hide_index=True, use_container_width=True)


def show_prop_analyzer(player):
    st.subheader(f"Prop Analyzer: {player.name}")
    st.write("Pick a stat and enter a line to see how often this player has gone over it.")

    # Fantasy points and share stats aren't sportsbook props
    prop_stats = [s for s in POSITION_STATS[player.position]
                  if s not in SHARE_STATS and s != "fantasy_points_ppr"]

    left, middle, right = st.columns(3)
    stat = left.selectbox("Stat", prop_stats, format_func=label)

    # Default line: the player's average rounded to the nearest .5 below it
    default_line = max(math.floor(player.average(stat)) + 0.5, 0.5)
    line = middle.number_input("Prop line", min_value=0.0, value=default_line, step=0.5,
                               key=f"line_{player.player_id}_{stat}")

    games = player.games_played()
    if games > 1:
        last_n = right.slider("Last N games", min_value=1, max_value=games, value=min(10, games))
    else:
        last_n = 1
        right.caption("Only 1 game played so far.")

    result = player.hit_rate(stat, line, last_n)

    cols = st.columns(4)
    cols[0].metric("Over", result["overs"])
    cols[1].metric("Under", result["unders"])
    cols[2].metric("Push", result["pushes"])
    cols[3].metric("Over rate", f"{result['over_rate']:.0%}")

    recent = player.recent_games(last_n)
    average = recent[stat].fillna(0).mean()
    st.write(f"Over his last **{result['games']}** games, {player.name} went **over "
             f"{line:g} {label(stat).lower()}** in **{result['overs']}** of them and "
             f"averaged **{average:.1f}**.")

    # Bar chart: each game is green if it went over the line, red if under
    chart = pd.DataFrame({"Week": recent["week"]})
    values = recent[stat].fillna(0)
    chart["Over"] = values.where(values > line, 0)
    chart["Under"] = values.where(values <= line, 0)
    st.bar_chart(chart, x="Week", y=["Over", "Under"], color=[OVER_COLOR, UNDER_COLOR])
    st.caption(f"Prop line: {line:g}. Past results don't guarantee future outcomes. "
               "This tool is for research only and does not place bets.")


def show_leaderboard(df, position):
    st.subheader(f"{position} Leaderboard")
    st.write("Players ranked by their per-game average in the stat you choose.")

    left, right = st.columns(2)
    stat = left.selectbox("Rank by", POSITION_STATS[position], format_func=label,
                          key="leaderboard_stat")
    max_games = int(df.groupby("player_id")["week"].count().max())
    min_games = right.slider("Minimum games played", 1, max_games, min(3, max_games))

    board = (df.groupby("player_id")
               .agg(Player=("player_display_name", "last"),
                    Team=("team", "last"),
                    Games=("week", "count"),
                    Average=(stat, "mean"))
               .query("Games >= @min_games")
               .sort_values("Average", ascending=False)
               .head(25)
               .reset_index(drop=True))
    board.index = board.index + 1  # rank starts at 1

    if stat in SHARE_STATS:
        board["Average"] = (board["Average"] * 100).round(1)
        board = board.rename(columns={"Average": f"{label(stat)} (%) per game"})
    else:
        board["Average"] = board["Average"].round(1)
        board = board.rename(columns={"Average": f"{label(stat)} per game"})

    st.dataframe(board, use_container_width=True)


# ---------- Main ----------

def main():
    st.title("Fourth & Data: NFL Analytics for Fantasy and Betting")
    st.write("Look up any NFL player's weekly stats, test how often they've cleared a "
             "player prop line, and see who leads the league in the stats that matter "
             "for fantasy football. Use the filters on the left to choose a season and position.")

    season, position, include_playoffs = show_sidebar()

    try:
        df = load_weekly_stats(season)
    except Exception as error:
        st.error("Couldn't load NFL stats right now. Check your internet connection and try again.")
        st.caption(f"Technical details: {type(error).__name__}: {error}")
        st.stop()

    if not include_playoffs:
        df = df[df["season_type"] == "REG"]
    df = df[df["position"] == position]

    if df.empty:
        st.warning("No games found for these filters yet.")
        st.stop()

    players = build_player_list(df)
    player_id = st.selectbox(
        "Choose a player", players.index,
        format_func=lambda pid: f"{players.loc[pid, 'name']} ({players.loc[pid, 'team']})",
        help="Players are listed by total fantasy points, best first. Start typing to search.",
    )
    player = Player(df[df["player_id"] == player_id])

    lookup_tab, prop_tab, board_tab = st.tabs(["Player Lookup", "Prop Analyzer", "Leaderboard"])
    with lookup_tab:
        show_player_lookup(player)
    with prop_tab:
        show_prop_analyzer(player)
    with board_tab:
        show_leaderboard(df, position)


main()
