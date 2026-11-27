# Pakistan Fantasy League — Dugout Fantasy Cricket

## Project Description

Pakistan Fantasy League is a Python-based fantasy cricket team management project developed as part of the Advanced Python for AI course.

The project uses real PSL player data to create and validate fantasy cricket teams. It includes player management, team validation, league rankings, JSON persistence, and a FastAPI REST API.

## Features

- Load 142 players from a CSV file.
- Display players by franchise and role.
- Create and manage fantasy cricket teams.
- Validate team size, budget, franchise limits, and player roles.
- Detect duplicate players.
- Validate captain and vice-captain selection.
- Calculate total and remaining credits.
- Load teams from CSV and JSON files.
- Save registered API teams to JSON.
- Display legal and illegal team results.
- Report six rejected teams from CSV and JSON files.
- Rank fantasy teams by credits.
- Provide a REST API using FastAPI.
- Provide a Python API client using Requests.
- Validate API requests using Pydantic.
- Persist registered teams across server restarts.

## Project Structure

```text
Pakistan Fantasy League/
│
├── data/
│   ├── players.csv
│   ├── sample_teams.csv
│   ├── my_team.csv
│   ├── bad_teams.csv
│   ├── bad_teams.json
│   ├── good_teams.json
│   └── my_bad_teams.json
│
├── dugout_waqar/
│   ├── __init__.py
│   ├── api.py
│   ├── errors.py
│   ├── loader.py
│   ├── models.py
│   └── rules.py
│
├── tests/
│   └── test_team_validation.py
│
├── main.py
├── call_api.py
├── match_report.py
├── requirements.txt
├── my_bad_teams.md
└── README.md
```

## Requirements

- Python 3.10 or newer
- pip
- Dependencies listed in `requirements.txt`

## Installation

Clone the repository and open its project directory.

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run the Main Program

Run the fantasy cricket validation and league ranking program:

```bash
python main.py
```

The program displays player statistics, team validation results, rejected CSV and JSON teams, and league rankings.

## Run the FastAPI Server

Start the API server from the project root directory:

```bash
uvicorn dugout_waqar.api:app --reload
```

The API runs at:

`http://127.0.0.1:8000`

## API Documentation

Open the interactive Swagger documentation in your browser:

`http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API status and data counts |
| GET | `/players` | List all players |
| GET | `/players?role=BAT` | Filter players by role |
| GET | `/players?franchise=Lahore Qalandars` | Filter players by franchise |
| GET | `/players/{player_id}` | Get one player |
| POST | `/teams` | Register a fantasy team |
| GET | `/teams` | List registered teams |
| GET | `/teams/{team_id}` | Get one fantasy team |
| GET | `/teams/{team_id}/credits` | Get team credit summary |

## Team Registration

The `POST /teams` endpoint accepts a JSON request containing:

- `team_name`
- `owner`
- `player_ids`
- `captain`
- `vice_captain`

The request must contain exactly 11 player IDs.

Successful team registration returns HTTP 201.

Error responses include:

- HTTP 400: Fantasy team validation failed.
- HTTP 404: Player or team was not found.
- HTTP 422: Request body validation failed.

Registered teams are saved in `data/teams.json` and loaded when the API starts.

The runtime file `data/teams.json` is not included in Git.

## Custom Illegal Team Tests — Deliverable 2, Part B2

Two custom illegal fantasy teams were created and submitted through the `POST /teams` API endpoint.

### 1. Duplicate Player Test

- Team name: `Duplicate Player Test`
- Violation: The same player appears twice.
- Expected response: HTTP 400.
- Result: PASS.

### 2. Same Captain and Vice-Captain Test

- Team name: `Same Captain Test`
- Violation: Captain and vice-captain are the same player.
- Expected response: HTTP 400.
- Result: PASS.

Test request bodies are stored in:

`data/my_bad_teams.json`

The actual API responses and test results are documented in:

`my_bad_teams.md`

Both tests confirmed that the API correctly rejects illegal fantasy teams.

## Python API Client

The project includes a Requests-based client for communicating with the FastAPI server.

Start the API server first, then run:

```bash
python call_api.py
```

## Run Tests

Run the unit tests using unittest:

```bash
python -m unittest discover -s tests -v
```

Run the tests using pytest:

```bash
python -m pytest -q
```

Current test results:

- unittest: 3 tests passed.
- pytest: 3 tests passed.

## Fantasy Team Rules

- Each team must contain exactly 11 players.
- Maximum budget is 100 credits.
- Maximum 7 players can belong to one franchise.
- WK: 1–2 players.
- BAT: 3–5 players.
- AR: 1–3 players.
- BOWL: 3–5 players.
- Duplicate players are not allowed.
- Captain and vice-captain must belong to the team.
- Captain and vice-captain must be different players.

## Data Files

Player and team information is stored in the `data/` directory.

The project includes CSV and JSON files for testing valid and invalid fantasy teams.

The API creates `data/teams.json` when teams are registered. This runtime file is not included in Git.

## Author

Waqar Ali
