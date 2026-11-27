TEAM_SIZE = 11
MAX_CREDITS = 100
MAX_FROM_ONE_FRANCHISE = 7
 
# role -> (minimum, maximum) number of players allowed in a team
ROLE_LIMITS = {
    "WK": (1, 2),
    "BAT": (3, 5),
    "AR": (1, 3),
    "BOWL": (3, 5),
}

def check_players_count(team):
    """The team must have exactly TEAM_SIZE players."""
    if len(team.players) != TEAM_SIZE:
        return [f"Team must have {TEAM_SIZE} players, but has {len(team.players)}"]
    return []
 
 
def check_budget(team):
    """The team's total credits must not exceed MAX_CREDITS."""
    total = team.total_credits()
    if total > MAX_CREDITS:
        return [f"Team has {total} credits, but maximum is {MAX_CREDITS}"]
    return []


def check_franchise_limit(team):
    """No more than MAX_FROM_ONE_FRANCHISE players from a single franchise."""
    errors = []
    for franchise, count in team.count_by_franchise().items():
        if count > MAX_FROM_ONE_FRANCHISE:
            errors.append(
                f"Team has {count} players from {franchise}, "
                f"but maximum is {MAX_FROM_ONE_FRANCHISE}"
            )
    return errors



def check_roles(team):
    """Each valid role must have between its minimum and maximum players."""
    counts = {role: 0 for role in ROLE_LIMITS}

    for player in team.players:
        if player.role in counts:
            counts[player.role] += 1

    errors = []

    for role, (low, high) in ROLE_LIMITS.items():
        count = counts[role]

        if count < low or count > high:
            errors.append(
                f"Team has {count} players with role {role}, "
                f"but must have between {low} and {high}"
            )

    return errors


def check_captains(team):
    """Captain and vice-captain must be chosen, be in the team, and be different."""
    # Stop early: the checks below would crash on None
    if team.captain is None or team.vice_captain is None:
        return ["Team must have both a captain and a vice-captain"]
 
    errors = []
    if team.captain not in team.players:
        errors.append(f"Captain {team.captain.name} is not in the team")
    if team.vice_captain not in team.players:
        errors.append(f"Vice-captain {team.vice_captain.name} is not in the team")
    if team.captain == team.vice_captain:
        errors.append("Captain and vice-captain cannot be the same player")
    return errors



def check_no_duplicates(team):
    """A team must not contain the same player more than once."""
    seen_players = set()
    errors = []

    for player in team.players:
        if player.player_id in seen_players:
            errors.append(
                f"Duplicate player found: {player.name} ({player.player_id})"
            )
        else:
            seen_players.add(player.player_id)

    return errors



def check_valid_roles(team):
    """Every player must have a valid role."""
    errors = []

    for player in team.players:
        if player.role not in ROLE_LIMITS:
            errors.append(
                f"Invalid player role: {player.role}"
            )

    return errors
