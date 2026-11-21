class League:
    def __init__(self, name):
        self.name = name
        self.teams = {}

    def add_team(self, team):
        self.teams[team.owner] = team

    def find_team(self, owner):
        return self.teams.get(owner)

    def legal_teams(self):
        return [team for team in self.teams.values() if not team.check_rules()]

    def rank_teams(self):
        return sorted(self.teams.values(), key=lambda team: team.total_credits())
