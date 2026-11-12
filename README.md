# Fourth & Data: NFL Analytics for Fantasy and Betting

## Student Name
Willem Donnelly

## App Description
Fourth & Data will be a Streamlit web app that collects NFL statistics in one
place, including the niche, highly predictive metrics that most fantasy and
sports-betting sites hide behind paywalls or leave out entirely. Beyond basic
stats like yards and touchdowns, it will show usage and efficiency metrics such
as target share, air yards share, snap share, red zone opportunities, and
expected points added (EPA). Users will be able to look up players and teams,
compare players side by side, and see how a player's recent performance stacks
up against a betting line or fantasy projection. The app is an analytics and
research tool. It does not place bets.

## Intended Users
This app is intended for fantasy football players who want an edge in lineup,
waiver, and trade decisions, and for sports bettors (21+) who research player
props and moneylines before making their own decisions. It is designed for
fans who want deeper data than a typical fantasy app shows, without needing to
write code or build spreadsheets themselves.

## Planned Features
- **Player lookup:** search any player and see season and week-by-week stats,
  including usage metrics like target share, snap share, and air yards.
- **Player comparison:** compare two or more players side by side to help with
  start/sit and trade decisions.
- **Player prop analyzer:** enter a prop line (for example, 64.5 receiving
  yards) and see how often the player has gone over that number this season
  and in recent games.
- **Matchup view:** see how each defense performs against each position
  (yards and fantasy points allowed) to spot favorable matchups.
- **Team moneyline view:** compare two teams' offensive and defensive
  efficiency (EPA per play, success rate) alongside the moneyline.
- **Future (machine learning):** predict player stat outcomes and compare the
  predictions to betting lines and fantasy projections.

## Course Concepts Used
- **Functions** to load, clean, and calculate stats (for example, a function
  that computes a player's hit rate over a prop line).
- **Loops** to process players, games, and weeks.
- **Object-oriented programming** with classes such as `Player` and `Team`
  that store stats and provide methods like `hit_rate(line)`.
- **Conditionals and input validation** for user selections and prop lines.
- **APIs and data** using public NFL data and, later, sports odds data.

## Planned Data Sources
- Public NFL play-by-play and player data from the nflverse project.
- Sports odds data from a public odds API (planned for a later phase).

## How to Run
1. Install the requirements:

       pip install -r requirements.txt

2. Start the app:

       streamlit run app.py

## Disclaimer
This app is for informational and educational purposes only. It does not place
bets or guarantee outcomes. Sports betting is only for adults of legal age in
jurisdictions where it is permitted.
