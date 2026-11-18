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
The app is organized into pages, grouped in the sidebar menu.

**Player Tools**
- **Player Lookup:** per-game averages, a fantasy-points-by-week chart, and a full
  game log with position-specific stats.
- **Prop Analyzer:** enter a prop line and a number of recent games to see overs,
  unders, pushes, the over rate, and a color-coded bar chart.
- **Leaderboard:** the top 25 players at a position by per-game average in any
  stat, with a minimum-games filter.

**Usage & Volume**
- **Target Shares:** each player's share of team targets, air yards share, and a
  trend column comparing the last 3 games to the season average, plus a weekly
  target share chart.
- **Snap Shares:** offensive snap share by player, plus a team grid showing how
  snaps split week by week.
- **Reception Rate:** catch rate, yards per target, and yards per reception, with
  a volume-vs-efficiency scatterplot.
- **Carries:** carries, carries per game, carry share of team rushing attempts,
  and a week-by-week backfield split for any team.

**League**
- **Schedule & Lines:** every game with final scores, the favorite and spread,
  the total, and both moneylines.

**Shared filters:** season (2026 or 2025) and whether to include playoff games
apply to every page.

## Planned Features (Final Version)
- **Phase 2 (fantasy and prop core):** QB target trees, red zone efficiency,
  goal-line and short-yardage roles, 3rd and 4th down usage, and directional run
  and pass splits, all built from play-by-play data.
- **Phase 3 (team context):** pace and play-calling, drive efficiency, an
  offensive line proxy, and turnover luck.
- **Phase 4 (extras):** kicker report, special teams and field position, penalty
  tracker, IDP defensive stats, player play logs, and game flow charts.
- **Phase 5:** ADP from an outside fantasy data source.
- **Player comparison** and **live betting lines** from a sports odds API.
- **Deployment** on Streamlit Community Cloud.
- **Machine learning:** predict player stat outcomes and compare them to prop
  lines and fantasy projections.

## Course Concepts Used
- **Object-oriented programming:** `player.py` defines a `Player` class with
  methods like `average(stat)` and `hit_rate(stat, line, last_n)`.
- **Loops and conditionals:** `hit_rate` and `target_share_table` loop through
  games and players and use `if/elif/else` logic.
- **Functions and modules:** calculations live in `metrics.py`, data loading in
  `data.py`, shared widgets in `common.py`, and each page in its own file.
- **Dictionaries:** stat labels, position settings, and page navigation.
- **Error handling:** `try/except` shows a friendly message if data can't load,
  and the loader falls back from Parquet to CSV if needed.

## Project Structure
| File | Purpose |
|---|---|
| `app.py` | Sets up page navigation and the shared sidebar filters |
| `app_pages/` | One file per page |
| `common.py` | Shared filters, safe data loading, and widgets |
| `data.py` | Downloads and caches nflverse data (weekly stats, snap counts, schedule, play-by-play) |
| `metrics.py` | All stat calculations (plain pandas, no Streamlit) |
| `player.py` | `Player` class |
| `requirements.txt` | Required packages |

## How to Run
1. Install the requirements:

       pip install -r requirements.txt

2. Start the app:

       streamlit run app.py

## Data Source and References
- NFL stats, snap counts, schedules, and play-by-play: nflverse public data,
  https://github.com/nflverse/nflverse-data
- Streamlit multipage apps: https://docs.streamlit.io/develop/concepts/multipage-apps
- Streamlit documentation: https://docs.streamlit.io
- pandas documentation: https://pandas.pydata.org/docs/

## Disclaimer
This app is for informational and educational purposes only. It does not place
bets or guarantee outcomes. Sports betting is only for adults of legal age in
jurisdictions where it is permitted.
