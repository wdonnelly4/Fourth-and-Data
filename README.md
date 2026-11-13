# Fourth & Data: NFL Analytics for Fantasy and Betting

## Student Name
Willem Donnelly

## App Description
Fourth & Data is a Streamlit web app that pulls real, weekly NFL player stats
and turns them into quick answers for fantasy football and player-prop
research. Users can look up any quarterback, running back, wide receiver, or
tight end and see their game-by-game production, including usage stats like
target share and air yards share that most fantasy apps don't show up front.
The Prop Analyzer lets users enter a betting line (for example, 64.5 receiving
yards) and instantly see how often that player has gone over it in recent
games. A leaderboard ranks players at each position by any stat. The data comes
from nflverse, a free public NFL data project, and updates as the season goes
on. The app is a research tool and does not place bets.

## Intended Users
This app is intended for fantasy football players who want an edge in lineup,
waiver, and trade decisions, and for sports bettors (21+) who research player
props before making their own decisions. It's built for fans who want deeper
data than a typical fantasy app shows, without needing to write code or build
spreadsheets themselves.

## Current Features (Implemented)
- **Live NFL data:** weekly stats for the 2026 and 2025 seasons, loaded from
  nflverse and cached for 6 hours so the app stays fast.
- **Filters:** choose a season, a position (QB, RB, WR, TE), and whether to
  include playoff games.
- **Player search:** a searchable dropdown of every player at that position,
  sorted by total fantasy points so the top players appear first.
- **Player Lookup:** per-game averages, a chart of fantasy points by week, and
  a full game log with position-specific stats (for example, target share for
  receivers and passing yards for quarterbacks).
- **Prop Analyzer:** pick a stat, enter a prop line, and choose how many recent
  games to look at. The app counts overs, unders, and pushes, shows the over
  rate, and draws a bar chart with each game colored by whether it went over (green)
  or under (red).
- **Leaderboard:** the top 25 players at a position ranked by per-game average
  in any stat, with a minimum-games filter so one big game doesn't skew the
  rankings.

## Planned Features (Final Version)
- **Player comparison:** compare two or more players side by side for start/sit
  and trade decisions.
- **Matchup view:** how each defense performs against each position (yards and
  fantasy points allowed) to spot favorable matchups.
- **Opponent-adjusted prop analysis:** filter a player's hit rate by home/away
  and by the strength of the opposing defense.
- **Team moneyline view:** compare two teams' offensive and defensive
  efficiency (EPA per play, success rate) alongside the moneyline.
- **Live betting lines:** pull current prop lines from a sports odds API
  instead of entering them by hand.
- **Deployment:** publish the app on Streamlit Community Cloud.
- **Future (machine learning):** predict player stat outcomes and compare the
  predictions to betting lines and fantasy projections.

## Course Concepts Used
- **Object-oriented programming:** `player.py` defines a `Player` class that
  stores a player's game log and has methods like `average(stat)` and
  `hit_rate(stat, line, last_n)`.
- **Loops and conditionals:** `hit_rate` loops through each game and uses
  `if/elif/else` to count overs, unders, and pushes.
- **Functions:** the app is organized into functions for each section
  (sidebar, lookup, prop analyzer, leaderboard), plus helper functions.
- **Dictionaries:** `data.py` maps stat columns to readable names and lists
  which stats belong to each position.
- **Error handling:** `try/except` shows a friendly message if the data can't
  be loaded.

## Project Structure
| File | Purpose |
|---|---|
| `app.py` | Streamlit interface and layout |
| `data.py` | Loads and caches NFL data; stat names and position settings |
| `player.py` | `Player` class with stat calculations |
| `requirements.txt` | Required packages |

## How to Run
1. Install the requirements:

       pip install -r requirements.txt

2. Start the app:

       streamlit run app.py

## Data Source and References
- NFL stats: nflverse public data, https://github.com/nflverse/nflverse-data
- Streamlit documentation: https://docs.streamlit.io
- pandas documentation: https://pandas.pydata.org/docs/

## Disclaimer
This app is for informational and educational purposes only. It does not place
bets or guarantee outcomes. Sports betting is only for adults of legal age in
jurisdictions where it is permitted.
