import csv
from pathlib import Path

from .rules import (
    check_budget,
    check_captains,
    check_franchise_limit,
    check_players_count,
    check_roles,
)


class Player:
    def __init__(self, player_id, name, role, franchise, credits):
        self.player_id = player_id
        self.name = name
        self.role = role
        self.franchise = franchise
        self.credits = float(credits)

    def __str__(self):
        return (
            f"{self.player_id}, Name: {self.name}, Role: {self.role}, "
            f"Franchise: {self.franchise}, Credits: {self.credits:g}"
        )


class FantasyTeam:
    def __init__(self, team_name, owner):
        self.team_name = team_name
        self.owner = owner
        self.players = []
        self.captain = None
        self.vice_captain = None

    def add_player(self, player):
        self.players.append(player)

    def total_credits(self):
        return sum(player.credits for player in self.players)

    def count_by_role(self):
        counts = {"WK": 0, "BAT": 0, "AR": 0, "BOWL": 0}
        for player in self.players:
            counts[player.role] += 1
        return counts

    def count_by_franchise(self):
        counts = {}
        for player in self.players:
            counts[player.franchise] = counts.get(player.franchise, 0) + 1
        return counts

    def set_captain(self, captain, vice_captain):
        self.captain = captain
        self.vice_captain = vice_captain

    def most_expensive(self):
        if not self.players:
            return None
        return max(self.players, key=lambda player: player.credits)

    def remaining_budget(self):
        return 100 - self.total_credits()

    def check_rules(self):
        errors = []
        errors.extend(check_players_count(self))
        errors.extend(check_budget(self))
        errors.extend(check_franchise_limit(self))
        errors.extend(check_roles(self))
        errors.extend(check_captains(self))
        return errors

    def __str__(self):
        return (
            f"{self.team_name} (owner: {self.owner}, "
            f"{len(self.players)} players, {self.total_credits():g} cr)"
        )


def load_players(csv_path):
    csv_path = Path(csv_path)
    players = {}
    with csv_path.open("r", newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            player = Player(
                row["player_id"], row["name"], row["role"],
                row["franchise"], row["credits"],
            )
            players[player.player_id] = player
    return players


def team_from_row(row, players):
    team = FantasyTeam(row["team_name"], row["owner"])
    for player_id in row["players"].split(";"):
        player_id = player_id.strip()
        if player_id:
            team.add_player(players[player_id])
    captain = players.get(row["captain"])
    vice_captain = players.get(row["vice_captain"])
    team.set_captain(captain, vice_captain)
    return team


def load_teams(path, players):
    teams = []
    with Path(path).open("r", newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            teams.append(team_from_row(row, players))
    return teams
