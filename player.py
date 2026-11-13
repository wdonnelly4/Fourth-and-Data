# player.py
# The Player class: one player's game log plus the calculations the app needs.


class Player:
    """Holds one player's weekly games and calculates stats from them."""

    def __init__(self, games):
        # games: a DataFrame with one row per game for this player
        self.games = games.sort_values("week").reset_index(drop=True)
        latest = self.games.iloc[-1]
        self.player_id = latest["player_id"]
        self.name = latest["player_display_name"]
        self.position = latest["position"]
        self.team = latest["team"]  # most recent team, in case of a trade

    def games_played(self):
        return len(self.games)

    def average(self, stat):
        """Average per game for a stat (missing values count as 0)."""
        return self.games[stat].fillna(0).mean()

    def recent_games(self, n):
        """The player's last n games."""
        return self.games.tail(n)

    def hit_rate(self, stat, line, last_n):
        """Count how many of the last n games went over or under a prop line."""
        overs = 0
        unders = 0
        pushes = 0

        for value in self.recent_games(last_n)[stat].fillna(0):
            if value > line:
                overs += 1
            elif value < line:
                unders += 1
            else:
                pushes += 1  # landed exactly on the line

        decided = overs + unders
        rate = overs / decided if decided > 0 else 0.0
        return {"overs": overs, "unders": unders, "pushes": pushes,
                "games": overs + unders + pushes, "over_rate": rate}
