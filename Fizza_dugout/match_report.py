import json
import sys

from dugout_waqar.matches import (
    batter_card,
    innings_runs,
    load_match,
    match_summary,
    top_scorers,
)


def main():
    # Read match file path from command line
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "data/matches/match_01.json"

    try:
        match = load_match(path)
    except FileNotFoundError:
        print(f"No match file at {path}")
        return
    except json.JSONDecodeError as error:
        print(f"{path} is not valid JSON: {error}")
        return

    summary = match_summary(match)
    home, away = summary["teams"]

    print(f"{home} v {away}")
    print(f"{summary['date']}, {summary['venue']}")

    for team, runs in innings_runs(match).items():
        print(f" {team}: {runs}")

    print(f"Winner: {summary['winner']} {summary['margin']}".rstrip())

    print("\nLeading scorers")
    for name, runs in top_scorers(match, 3):
        card = batter_card(match, name)
        print(
            f" {name:22s} {card['runs']:3d} off {card['balls']:3d} balls"
            f" 4s: {card['fours']:2d} 6s: {card['sixes']:2d}"
        )


if __name__ == "__main__":
    main()