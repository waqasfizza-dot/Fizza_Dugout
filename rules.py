TEAM_SIZE = 11
MAX_CREDITS = 100
MAX_FROM_ONE_FRANCHISE = 7

ROLE_LIMITS = {
    "WK": (1, 2),
    "BAT": (3, 5),
    "AR": (1, 3),
    "BOWL": (3, 5),
}


def check_players_count(team):
    if len(team.players) != TEAM_SIZE:
        return [f"Team must have {TEAM_SIZE} players, but has {len(team.players)}"]
    return []


def check_budget(team):
    total = team.total_credits()
    if total > MAX_CREDITS:
        return [f"Team has {total:g} credits, but maximum is {MAX_CREDITS}"]
    return []


def check_franchise_limit(team):
    errors = []
    for franchise, count in team.count_by_franchise().items():
        if count > MAX_FROM_ONE_FRANCHISE:
            errors.append(
                f"Team has {count} players from {franchise}, "
                f"but maximum is {MAX_FROM_ONE_FRANCHISE}"
            )
    return errors


def check_roles(team):
    counts = team.count_by_role()
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
