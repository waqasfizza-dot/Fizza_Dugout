"""The Dugout web API."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from dugout_waqar.loader import (
    load_players,
    load_teams_json,
    save_teams_json,
)
from dugout_waqar.models import FantasyTeam
from dugout_waqar.errors import (
    PlayerNotFoundError,
    InvalidTeamError,
)

class TeamIn(BaseModel):
    """The shape of the JSON body that POST /teams expects."""

    team_name: str
    owner: str
    player_ids: list[str] = Field(min_length=11, max_length=11)
    captain: str
    vice_captain: str

PLAYERS_CSV = "data/players.csv"
TEAMS_JSON = "data/teams.json"

app = FastAPI(
    title="Dugout API",
    version="2.0",
    description="Browse the PSL player pool.",
)

# Loaded once, when the server starts, not on every request
players = load_players(PLAYERS_CSV)
teams = {}

try:
    saved_teams = load_teams_json(TEAMS_JSON, players)
    for team in saved_teams:
        team_id = len(teams) + 1
        teams[team_id] = team
except FileNotFoundError:
    pass

@app.get("/health")
def health():
    """Say that the server is up and report loaded data."""
    return {
        "status": "ok",
        "players": len(players),
        "teams": len(teams),
    }

def team_details(team_id, team):
    """Return a team with its id and calculated details."""

    return {
        "team_id": team_id,
        "team_name": team.team_name,
        "owner": team.owner,
        "player_count": len(team.players),
        "players": [player.to_dict() for player in team.players],
        "captain": team.captain.name if team.captain else None,
        "vice_captain": team.vice_captain.name if team.vice_captain else None,
        "total_credits": team.total_credits(),
        "remaining_credits": team.remaining_credits(),
        "count_by_role": team.count_by_role(),
    }

@app.get("/players")
def list_players(role: str | None = None, franchise: str | None = None):
    """Return the player pool, filtered by role and franchise if asked."""
    found = []
    for player in players.values():
        if role and player.role != role.upper():
            continue
        if franchise and player.franchise.lower() != franchise.lower():
            continue
        found.append(player.to_dict())
    return {"count": len(found), "players": found}

@app.get("/players/{player_id}")
def get_player(player_id: str):
    """Return one player by id, or 404 if there is no such player."""
    if player_id not in players:
        raise HTTPException(status_code=404, detail=f"No player with id {player_id}")
    return players[player_id].to_dict()

@app.post("/teams", status_code=201)
def register_team(team_in: TeamIn):
    """Register a new fantasy team."""

    try:
        team = FantasyTeam.from_dict(team_in.model_dump(), players)
    except PlayerNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

    try:
        team.validate()
    except InvalidTeamError as error:
        raise HTTPException(
            status_code=400,
            detail={
                "message": str(error),
                "problems": error.problems,
            },
        )

    team_id = max(teams.keys(), default=0) + 1
    teams[team_id] = team

    save_teams_json(TEAMS_JSON, list(teams.values()))

    return team_details(team_id, team)

@app.get("/teams")
def list_teams():
    """Return all registered fantasy teams."""

    return {
        "count": len(teams),
        "teams": [
            team_details(team_id, team)
            for team_id, team in teams.items()
        ],
    }

@app.get("/teams/{team_id}")
def get_team(team_id: int):
    """Return one registered team."""

    if team_id not in teams:
        raise HTTPException(
            status_code=404,
            detail=f"No team with id {team_id}",
        )

    return team_details(team_id, teams[team_id])

@app.get("/teams/{team_id}/credits")
def get_team_credits(team_id: int):
    """Return the credit summary of one fantasy team."""

    if team_id not in teams:
        raise HTTPException(
            status_code=404,
            detail=f"No team with id {team_id}",
        )

    team = teams[team_id]

    return {
        "team_id": team_id,
        "team_name": team.team_name,
        "total_credits": team.total_credits(),
        "remaining_credits": team.remaining_credits(),
    }