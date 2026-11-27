import csv
import json
from dugout_waqar.models import Player, FantasyTeam, find_player


def load_players(path):
    """Load players from CSV and validate player records."""
    players = {}

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:

            # Remove unnecessary spaces from CSV values
            row = {
                key: value.strip() if value is not None else ""
                for key, value in row.items()
            }

            # Check that player ID exists
            player_id = row.get("player_id")

            if not player_id:
                raise ValueError(
                    "Player ID is missing in CSV file"
                )

            # Check for duplicate player IDs
            if player_id in players:
                raise ValueError(
                    f"Duplicate player ID found: {player_id}"
                )

            # Convert CSV row into Player object
            player = Player.form_row(row)

            # Store player using unique ID
            players[player.player_id] = player

    return players



def team_from_row(row, players):
    """Create a FantasyTeam from a CSV row with data validation."""

    # Clean team name and owner
    team_name = (row.get("team_name") or "").strip()
    owner = (row.get("owner") or "").strip()

    if not team_name:
        raise ValueError("Team name is missing in CSV file")

    if not owner:
        raise ValueError("Team owner is missing in CSV file")

    # Create fantasy team
    team = FantasyTeam(team_name, owner)

    # Read and clean player IDs
    player_ids = (row.get("players") or "").split(";")

    for player_id in player_ids:
        player_id = player_id.strip()

        if not player_id:
            continue

        team.add_player(find_player(players, player_id))

    # Read captain and vice-captain IDs
    captain_id = (row.get("captain") or "").strip()
    vice_captain_id = (row.get("vice_captain") or "").strip()

    # Validate captain ID
    captain = find_player(players, captain_id)

    # Validate vice-captain ID
    vice_captain = find_player(players, vice_captain_id)
    # Assign captain and vice-captain
    team.set_captain(captain, vice_captain)

    return team


def load_team(path, players):
    # Return the first team in a teams CSV file, or None if the file has no teams.
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            return team_from_row(row, players)  # return on the first row only
    return None

def load_teams(path, players):
    """Return a list of every team in a teams CSV file."""
    teams = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            teams.append(team_from_row(row, players))
    return teams


# main.py: change the import line at the top to
# from dugout_waqar.loader import load_players, load_teams


def read_team_rows(path):
    """Return the raw rows of a teams CSV file, without building any teams."""

    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_team_entries(path):
    """Return the raw entries of a teams JSON file,
    without building any teams."""

    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_teams_json(path, teams):
    """Write a list of FantasyTeams to a JSON file."""

    data = [team.to_dict() for team in teams]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_teams_json(path, players):
    """Load teams from a JSON file and return FantasyTeam objects."""

    entries = read_team_entries(path)

    teams = []

    for entry in entries:
        team = FantasyTeam.from_dict(entry, players)
        teams.append(team)

    return teams