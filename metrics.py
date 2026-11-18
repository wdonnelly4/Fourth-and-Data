# metrics.py
# All stat calculations live here. These are plain pandas functions with no
# Streamlit code, so they're easy to test and can feed a machine learning model later.

import pandas as pd


def regular_season_only(df, include_playoffs):
    """Drop playoff games unless the user asked for them."""
    if include_playoffs or "season_type" not in df.columns:
        return df
    return df[df["season_type"] == "REG"]


def filter_players(df, positions, team=None):
    """Keep only the chosen positions and, optionally, one team."""
    df = df[df["position"].isin(positions)]
    if team:
        df = df[df["team"] == team]
    return df


def weekly_trend(weekly, player_id, stat, as_percent=False):
    """One player's stat by week, for line charts."""
    games = weekly[weekly["player_id"] == player_id].sort_values("week")
    values = games[stat].fillna(0) * (100 if as_percent else 1)
    return pd.DataFrame({"Week": games["week"].values, "Value": values.values})


# ---------- Target share ----------

def target_share_table(weekly, positions, team=None, min_games=1):
    """Average target share per player, plus their last-3-games share to show trends."""
    df = filter_players(weekly, positions, team).sort_values("week")

    rows = []
    for player_id, games in df.groupby("player_id"):
        if len(games) < min_games:
            continue
        shares = games["target_share"].fillna(0) * 100
        latest = games.iloc[-1]
        season_share = shares.mean()
        last3_share = shares.tail(3).mean()
        rows.append({
            "player_id": player_id,
            "Player": latest["player_display_name"],
            "Team": latest["team"],
            "Pos": latest["position"],
            "Games": len(games),
            "Targets": int(games["targets"].fillna(0).sum()),
            "Targets / Game": games["targets"].fillna(0).mean(),
            "Target Share %": season_share,
            "Last 3 Games %": last3_share,
            "Trend": last3_share - season_share,
            "Air Yards Share %": (games["air_yards_share"].fillna(0) * 100).mean(),
        })

    table = pd.DataFrame(rows)
    if table.empty:
        return table
    return table.sort_values("Target Share %", ascending=False).reset_index(drop=True)


# ---------- Snap share ----------

def snap_share_table(snaps, positions, team=None, min_games=1):
    """Average offensive snap share per player."""
    df = filter_players(snaps, positions, team).sort_values("week")

    table = (df.groupby("pfr_player_id")
               .agg(Player=("player", "last"),
                    Team=("team", "last"),
                    Pos=("position", "last"),
                    Games=("week", "count"),
                    Snaps=("offense_snaps", "sum"),
                    avg_pct=("offense_pct", "mean"),
                    last_pct=("offense_pct", "last"))
               .reset_index())
    table = table[table["Games"] >= min_games]
    table["Snap Share %"] = table.pop("avg_pct") * 100
    table["Last Game %"] = table.pop("last_pct") * 100
    return table.sort_values("Snap Share %", ascending=False).reset_index(drop=True)


def team_snap_grid(snaps, team, positions):
    """Each player's snap share by week for one team (players as rows, weeks as columns)."""
    df = filter_players(snaps, positions, team)
    grid = df.pivot_table(index=["player", "position"], columns="week",
                          values="offense_pct", aggfunc="mean") * 100
    grid["Avg"] = grid.mean(axis=1)
    grid = grid.sort_values("Avg", ascending=False)
    grid.columns = [f"Wk {c}" if isinstance(c, (int, float)) and c == int(c) else c
                    for c in grid.columns]
    return grid.reset_index().rename(columns={"player": "Player", "position": "Pos"})


# ---------- Reception rate ----------

def reception_rate_table(weekly, positions, team=None, min_targets=1):
    """Catch rate and efficiency for every pass catcher with enough targets."""
    df = filter_players(weekly, positions, team).sort_values("week")

    table = (df.groupby("player_id")
               .agg(Player=("player_display_name", "last"),
                    Team=("team", "last"),
                    Pos=("position", "last"),
                    Games=("week", "count"),
                    Targets=("targets", "sum"),
                    Receptions=("receptions", "sum"),
                    Yards=("receiving_yards", "sum"))
               .reset_index())
    table = table[table["Targets"] >= max(min_targets, 1)].copy()
    table["Catch Rate %"] = table["Receptions"] / table["Targets"] * 100
    table["Yards / Target"] = table["Yards"] / table["Targets"]
    table["Yards / Reception"] = (table["Yards"] / table["Receptions"]).where(table["Receptions"] > 0, 0)
    return table.sort_values("Catch Rate %", ascending=False).reset_index(drop=True)


# ---------- Carries ----------

def carries_table(weekly, positions, team=None, min_games=1):
    """Rushing volume per player, including carry share: the percent of their
    team's carries they handled in the games they played."""
    # Total team carries in each game (all positions)
    team_carries = (weekly.groupby(["team", "week"])["carries"].sum()
                          .rename("team_carries").reset_index())
    df = filter_players(weekly, positions, team).merge(team_carries, on=["team", "week"])
    df = df.sort_values("week")

    table = (df.groupby("player_id")
               .agg(Player=("player_display_name", "last"),
                    Team=("team", "last"),
                    Pos=("position", "last"),
                    Games=("week", "count"),
                    Carries=("carries", "sum"),
                    team_carries=("team_carries", "sum"),
                    Yards=("rushing_yards", "sum"),
                    TDs=("rushing_tds", "sum"))
               .reset_index())
    table = table[(table["Games"] >= min_games) & (table["Carries"] > 0)].copy()
    table["Carries / Game"] = table["Carries"] / table["Games"]
    table["Carry Share %"] = table["Carries"] / table.pop("team_carries") * 100
    table["Yards / Carry"] = table["Yards"] / table["Carries"]
    return table.sort_values("Carries", ascending=False).reset_index(drop=True)


def team_carries_grid(weekly, team):
    """Each player's carries by week for one team."""
    df = weekly[(weekly["team"] == team) & (weekly["carries"].fillna(0) > 0)]
    grid = df.pivot_table(index=["player_display_name", "position"], columns="week",
                          values="carries", aggfunc="sum", fill_value=0)
    grid["Total"] = grid.sum(axis=1)
    grid = grid.sort_values("Total", ascending=False)
    grid.columns = [f"Wk {c}" if c != "Total" else c for c in grid.columns]
    return grid.reset_index().rename(columns={"player_display_name": "Player", "position": "Pos"})


# ---------- Schedule ----------

def _favorite(row):
    """nflverse spread_line is from the home team's view: positive = home favored."""
    spread = row["spread_line"]
    if pd.isna(spread):
        return ""
    if spread > 0:
        return f"{row['home_team']} -{spread:g}"
    if spread < 0:
        return f"{row['away_team']} -{-spread:g}"
    return "Pick'em"


def _score(row):
    if pd.isna(row["home_score"]):
        return ""
    return (f"{row['away_team']} {int(row['away_score'])} - "
            f"{int(row['home_score'])} {row['home_team']}")


def schedule_table(games, season, team=None, week=None):
    """Games for a season, optionally filtered to one team and/or week."""
    df = games[games["season"] == season].copy()
    if team:
        df = df[(df["home_team"] == team) | (df["away_team"] == team)]
    if week:
        df = df[df["week"] == week]

    table = pd.DataFrame({
        "Week": df["week"],
        "Date": df["gameday"],
        "Kickoff (ET)": df["gametime"],
        "Away": df["away_team"],
        "Home": df["home_team"],
        "Final": df.apply(_score, axis=1),
        "Favorite": df.apply(_favorite, axis=1),
        "Total": df["total_line"],
        "Away ML": df["away_moneyline"],
        "Home ML": df["home_moneyline"],
        "Roof": df["roof"],
    })
    return table.sort_values(["Week", "Date", "Kickoff (ET)"]).reset_index(drop=True)
