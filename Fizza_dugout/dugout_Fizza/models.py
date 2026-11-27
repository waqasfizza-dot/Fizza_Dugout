from dugout_waqar.errors import InvalidTeamError, PlayerNotFoundError

from dugout_waqar.rules import (
    check_players_count,
    check_budget,
    check_franchise_limit,
    check_roles,
    check_captains,
    check_no_duplicates,
    check_valid_roles,
)

def find_player(players, player_id):
    """Return the Player with this id, or raise PlayerNotFoundError."""

    if player_id not in players:
        raise PlayerNotFoundError(player_id)

    return players[player_id]



class Player:
    #constructor
    def __init__(self, player_id, name, role, franchise, credits):
        self.player_id = player_id
        self.name = name
        self.role = role
        self.franchise = franchise
        self.credits = credits

    @classmethod
    def form_row(cls, row):
        return cls(
            row["player_id"],
            row["name"],
            row["role"],
            row["franchise"],
            float(row["credits"]),
        )


    def to_dict(self):
        """Return this player as a dict, ready to be turned into JSON."""

        return {
            "player_id": self.player_id,
            "name": self.name,
            "franchise": self.franchise,
            "role": self.role,
            "credits": self.credits,
        }


    def __str__(self):
        return f"{self.name} ({self.franchise}, {self.role},{self.credits} cr)"


class FantasyTeam:
    def __init__(self, team_name, owner):
        self.team_name = team_name
        self.owner = owner
        self.players = []
        self.captain = None
        self.vice_captain = None

    def add_player(self,player):
        self.players.append(player)

    def total_credits(self):
        total = 0
        for player in self.players:
            total = total + player.credits
        return total


    def remaining_credits(self):
        """Return the credits remaining from the maximum team budget."""
        return 100 - self.total_credits()


    def count_by_role(self):
        counts = {
            "WK":0,
            "BAT":0,
            "AR":0,
            "BOWL":0
        }
        for player in self.players:
            counts[player.role] = counts[player.role] + 1
        return counts

    def set_captain(self, captain, vice_captain):
        self.captain = captain
        self.vice_captain = vice_captain


    def to_dict(self):
        """Return this team, ready to save."""

        return {
            "team_name": self.team_name,
            "owner": self.owner,
            "player_ids": [p.player_id for p in self.players],
            "captain": self.captain.player_id if self.captain else None,
            "vice_captain": self.vice_captain.player_id if self.vice_captain else None,
        }



    @classmethod
    def from_dict(cls, data, players):
        """Create a FantasyTeam from a dictionary."""

        team = cls(data["team_name"], data["owner"])

        for player_id in data["player_ids"]:
            player = find_player(players, player_id)
            team.add_player(player)

        captain_id = data.get("captain")
        vice_captain_id = data.get("vice_captain")

        if captain_id and vice_captain_id:
            team.set_captain(
                find_player(players, captain_id),
                find_player(players, vice_captain_id),
            )

        return team




    def count_by_franchise(self):
        """Return a dict of franchise name -> number of players from it."""
        counts = {}
        for player in self.players:
            # .get(key, 0) gives 0 the first time we see a franchise
            counts[player.franchise] = counts.get(player.franchise, 0) + 1
        return counts



    def check_rules(self):
        """Return a list of rule violations. An empty list means the team is legal."""
        errors = []
        errors.extend(check_players_count(self))
        errors.extend(check_budget(self))
        errors.extend(check_franchise_limit(self))
        errors.extend(check_no_duplicates(self))
        errors.extend(check_valid_roles(self))
        errors.extend(check_roles(self))
        errors.extend(check_captains(self))
        return errors


    def __str__(self):
        size = len(self.players)
        cost = self.total_credits()
        return f"{self.team_name}(owner: {self.owner},{size} player, {cost} cr)"

    def validate(self):
        """Raise InvalidTeamError if the team breaks any rule."""

        problems = self.check_rules()

        if problems:
            raise InvalidTeamError(self.team_name, problems)


class League:
    """A collection of FantasyTeams, with methods to look up and rank them."""

    def __init__(self, name):
        self.name = name
        self.teams = {}  # owner name -> FantasyTeam

    def add_team(self, team):
        self.teams[team.owner] = team

    def find_team(self, owner):
        """Return the FantasyTeam for the given owner, or None if not found."""
        return self.teams.get(owner)

    def legal_teams(self):
        """Return a list of the teams that break no rules."""
        return [team for team in self.teams.values() if not team.check_rules()]

    def rank_teams(self):
        """Return a list of teams sorted by total credits (lowest first)."""
        # self.teams is a dict, so sort its values (the teams), not its keys
        return sorted(self.teams.values(), key=lambda team: team.total_credits())
