"""The errors Dugout raises when something is wrong."""

class DugoutError(Exception):
    """Base class for every error raised by Dugout."""

class PlayerNotFoundError(DugoutError):
    """Raised when a player id is not in the player pool."""

    def __init__(self, player_id):
        super().__init__(f"No player with id {player_id}")
        self.player_id = player_id

class InvalidTeamError(DugoutError):
    """Raised when a team breaks a rule."""

    def __init__(self, team_name, problems):
        super().__init__(
            f"{team_name} is not a legal team: "
            + "; ".join(problems))
        self.team_name = team_name
        self.problems = problems
