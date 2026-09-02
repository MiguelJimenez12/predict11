import unittest
from unittest.mock import patch

from app.schemas.head_to_head import HeadToHead
from app.schemas.statistics import Statistics
from app.services.prediction_service import predict_match


def stats(team_id, name, wins, draws, losses, goals_for, goals_against):
    return Statistics(
        team_id=team_id, team_name=name, league="Liga MX", season=2026,
        matches_played=wins + draws + losses, wins=wins, draws=draws,
        losses=losses, goals_for=goals_for, goals_against=goals_against,
        clean_sheets=4, failed_to_score=2,
    )


class PredictionTest(unittest.TestCase):
    @patch("app.services.prediction_service.get_head_to_head")
    @patch("app.services.prediction_service.get_statistics")
    def test_probabilities_are_valid(self, get_statistics, get_head_to_head):
        get_statistics.side_effect = [stats(1, "Pumas", 8, 3, 2, 26, 12), stats(2, "America", 6, 4, 3, 21, 15)]
        get_head_to_head.return_value = [HeadToHead(fixture_id=1, home_team="Pumas", away_team="America", home_goals=2, away_goals=1, date="2026-01-01")]
        result = predict_match(1, 2)
        total = result.home_win_probability + result.draw_probability + result.away_win_probability
        self.assertAlmostEqual(total, 100.0)
        self.assertTrue(all(0 <= value <= 100 for value in [result.home_win_probability, result.draw_probability, result.away_win_probability]))
        self.assertEqual(result.data_source, "API-Football")

    def test_same_team_is_rejected(self):
        with self.assertRaises(ValueError):
            predict_match(1, 1)


if __name__ == "__main__":
    unittest.main()
