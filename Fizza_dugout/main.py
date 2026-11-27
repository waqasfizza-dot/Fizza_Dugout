
from dugout_waqar.loader import (
    load_players,
    load_team,
    load_teams,
    read_team_rows,
    read_team_entries,
    team_from_row,
)

from dugout_waqar.models import FantasyTeam, League

from dugout_waqar.errors import (
    InvalidTeamError,
    PlayerNotFoundError,
)

def show_pool(players):
    """Print how many players there are per franchise and per role."""
    by_franchise = {}
    by_role = {}
    for player in players.values():
        # .get(key, 0) gives 0 the first time we see a key, then we add 1
        by_franchise[player.franchise] = by_franchise.get(player.franchise, 0) + 1
        by_role[player.role] = by_role.get(player.role, 0) + 1
    print("Players by franchise:")
    for franchise in sorted(by_franchise):
        print(f"  {franchise}: {by_franchise[franchise]}")
    print("Players by role:")
    for role in sorted(by_role):
        print(f"  {role}: {by_role[role]}")

def show_team(team):
    """Print a team's players, cost and captains."""
    print(f"\nTeam {team.team_name} by {team.owner}:")
    for player in team.players:
        print(f"  {player}")
    print(f"Total credits: {team.total_credits()}")
    print(f"Captain: {team.captain.name}, Vice-captain: {team.vice_captain.name}")


def create_custom_test_teams(my_team):
    """Create two custom teams with separate rule violations."""

    # Test Team 1: Duplicate player
    duplicate_team = FantasyTeam(
        "Custom Test Team 1",
        "Custom Test Owner 1"
    )

    for player in my_team.players:
        duplicate_team.add_player(player)

    duplicate_pair_found = False

    # Find two non-captain players with the same role.
    # The duplicate player's credits must not exceed
    # the player being replaced.
    for duplicate_player in duplicate_team.players:
        if duplicate_player in (
            my_team.captain,
            my_team.vice_captain
        ):
            continue

        for replaced_player in duplicate_team.players:
            if replaced_player in (
                my_team.captain,
                my_team.vice_captain
            ):
                continue

            if (
                duplicate_player.role == replaced_player.role
                and duplicate_player.player_id != replaced_player.player_id
                and duplicate_player.credits <= replaced_player.credits
            ):
                duplicate_team.players.remove(replaced_player)
                duplicate_team.add_player(duplicate_player)
                duplicate_pair_found = True
                break

        if duplicate_pair_found:
            break

    if not duplicate_pair_found:
        raise ValueError(
            "Could not create a duplicate test team"
        )

    duplicate_team.set_captain(
        my_team.captain,
        my_team.vice_captain
    )

    # Test Team 2: Same captain and vice-captain
    captain_team = FantasyTeam(
        "Custom Test Team 2",
        "Custom Test Owner 2"
    )

    for player in my_team.players:
        captain_team.add_player(player)

    captain_team.set_captain(
        my_team.captain,
        my_team.captain
    )

    return [duplicate_team, captain_team]


def show_custom_test_teams(test_teams):
    """Display custom test teams and their rule violations."""

    print("\n========== CUSTOM TEST TEAMS ==========")

    for team in test_teams:
        print(f"\nTeam: {team.team_name}")

        errors = team.check_rules()

        if errors:
            print("ILLEGAL:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("LEGAL")

def show_ranking_table(league, players):
    """Display rejected teams and fantasy league rankings."""

    # Report rejected teams one by one

    print("\nThe six teams the league office could not accept")

    print("\n========== BAD TEAMS FROM CSV ==========")
    for row in read_team_rows("data/bad_teams.csv"):
        report_on_row(row, players)

    print("\n========== BAD TEAMS FROM JSON ==========")
    for entry in read_team_entries("data/bad_teams.json"):
        report_on_json_entry(entry, players)

    print("\nDone. Six CSV teams and six JSON teams were checked.")

    print("\n========== FANTASY LEAGUE RANKINGS ==========")
    print(
        f"{'Rank':<6}"
        f"{'Team Name':<25}"
        f"{'Owner':<22}"
        f"{'Credits':<10}"
        f"{'Verdict'}"
    )
    print("-" * 75)

    for rank, team in enumerate(league.rank_teams(), start=1):
        errors = team.check_rules()
        verdict = "ILLEGAL" if errors else "LEGAL"

        print(
            f"{rank:<6}"
            f"{team.team_name:<25}"
            f"{team.owner:<22}"
            f"{team.total_credits():<10.1f}"
            f"{verdict}"
        )


def main():
    players = load_players("data\\players.csv")
    show_pool(players)
    teams = load_teams("data\\sample_teams.csv", players)
    my_team = load_team("data\\my_team.csv", players)
    test_teams = create_custom_test_teams(my_team)
    show_custom_test_teams(test_teams)
        # Create fantasy league
    league = League("Pakistan Fantasy League")

    # Add all six sample teams
    for team in teams:
        league.add_team(team)

    # Add both custom test teams
    for team in test_teams:
        league.add_team(team)

    # Add personal fantasy team
    league.add_team(my_team)
    legal = []
    illegal = []
    for team in teams:
        show_team(team)
        errors = team.check_rules()
        if errors:
            illegal.append(team)
            print("ILLEGAL:")
            for error in errors:
                print(f"  - {error}")
        else:
            legal.append(team)
            print("LEGAL")
    print(f"\nSummary: {len(legal)} legal, {len(illegal)} illegal out of {len(teams)} teams")
    print("Legal teams:")

    for team in legal:
        print(f"  {team.team_name}")
    print("Illegal teams:")

    for team in illegal:
        print(f"  {team.team_name}")

    # Display personal fantasy team
    print("\n========== MY FANTASY TEAM ==========")

    show_team(my_team)

    print(f"Remaining credits: {my_team.remaining_credits()}")

    errors = my_team.check_rules()

    if errors:
        print("MY TEAM: ILLEGAL")
        for error in errors:
            print(f"  - {error}")
    else:
        print("MY TEAM: LEGAL")

    # Display fantasy league ranking table
    show_ranking_table(league, players)


def report(team_name, problems):
    """Print one verdict. An empty list of problems means the team is legal."""

    if not problems:
        print(f"  {team_name}: LEGAL")
        return

    print(f"  {team_name}: REJECTED")
    for problem in problems:
        print(f"    - {problem}")


def report_on_row(row, players):
    """Build one team from a CSV row and say whether it is legal."""

    try:
        team = team_from_row(row, players)
        team.validate()
    except PlayerNotFoundError as error:
        report(row["team_name"], [str(error)])
    except InvalidTeamError as error:
        report(error.team_name, error.problems)
    else:
        report(team.team_name, [])


def report_on_json_entry(entry, players):
    """Build a team from a JSON entry and report whether it is legal."""

    try:
        team = FantasyTeam.from_dict(entry, players)
        team.validate()

    except PlayerNotFoundError as error:
        report(entry["team_name"], [str(error)])

    except InvalidTeamError as error:
        report(error.team_name, error.problems)

    else:
        report(team.team_name, [])

if __name__ == "__main__":
    main()

