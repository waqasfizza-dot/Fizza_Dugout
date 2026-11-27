
import unittest

from dugout_waqar.models import Player, FantasyTeam


def create_valid_team():
    """Create a valid fantasy team for testing."""

    team = FantasyTeam("Test Team", "Test Owner")

    players = [
        Player("P001", "Player 1", "WK", "Lahore", 8),
        Player("P002", "Player 2", "BAT", "Karachi", 8),
        Player("P003", "Player 3", "BAT", "Multan", 8),
        Player("P004", "Player 4", "BAT", "Islamabad", 8),
        Player("P005", "Player 5", "AR", "Peshawar", 8),
        Player("P006", "Player 6", "AR", "Quetta", 8),
        Player("P007", "Player 7", "BOWL", "Lahore", 8),
        Player("P008", "Player 8", "BOWL", "Karachi", 8),
        Player("P009", "Player 9", "BOWL", "Multan", 8),
        Player("P010", "Player 10", "BOWL", "Islamabad", 8),
        Player("P011", "Player 11", "BOWL", "Peshawar", 8),
    ]

    for player in players:
        team.add_player(player)

    team.set_captain(players[1], players[0])

    return team


class TestFantasyTeamValidation(unittest.TestCase):

    def test_valid_team(self):
        """A valid team should have no rule errors."""

        team = create_valid_team()

        self.assertEqual(team.check_rules(), [])

    def test_duplicate_player(self):
        """A team should not contain the same player twice."""

        team = create_valid_team()
        team.add_player(team.players[0])

        errors = team.check_rules()

        self.assertIn(
            "Duplicate player found: Player 1 (P001)",
            errors
        )
        

    def test_same_captain_and_vice_captain(self):
        """Captain and vice-captain must be different players."""

        team = create_valid_team()
        team.set_captain(team.players[0], team.players[0])

        errors = team.check_rules()

        self.assertIn(
            "Captain and vice-captain cannot be the same player",
            errors
        )


if __name__ == "__main__":
    unittest.main()
