"""A Python client for the Dugout API."""

import requests

BASE_URL = "http://127.0.0.1:8000"

def check_health():
    """Check whether the Dugout API is running."""

    response = requests.get(f"{BASE_URL}/health")

    print("Status Code:", response.status_code)
    print("Response:", response.json())


def list_players():
    """Get all players from the Dugout API."""

    response = requests.get(f"{BASE_URL}/players")

    print("Status Code:", response.status_code)

    data = response.json()

    print("Total Players:", data["count"])

    for player in data["players"]:
        print(player["name"], "-", player["role"])


def get_player(player_id):
    """Get one player by their ID."""

    response = requests.get(f"{BASE_URL}/players/{player_id}")

    print("Status Code:", response.status_code)
    print("Player:", response.json())


def list_teams():
    """Get all registered fantasy teams."""

    response = requests.get(f"{BASE_URL}/teams")

    print("Status Code:", response.status_code)

    data = response.json()

    print("Total Teams:", data["count"])

    for team in data["teams"]:
        print(team["team_id"], "-", team["team_name"], "-", team["owner"])


def get_team(team_id):
    """Get one fantasy team by its ID."""

    response = requests.get(f"{BASE_URL}/teams/{team_id}")

    print("Status Code:", response.status_code)
    print("Team Details:", response.json())


if __name__ == "__main__":
    check_health()
    list_players()
    get_player("P089")
    list_teams()
    get_team(1)
    get_team(99)