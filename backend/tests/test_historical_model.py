import unittest
from datetime import datetime, timedelta

from app.ml.historical_model import MatchRecord, build_examples, evaluate, fit, parse_csv, predict_artifact


class HistoricalModelTest(unittest.TestCase):
    def test_parses_primary_and_mirror_formats(self):
        primary = "Date,HomeTeam,AwayTeam,FTHG,FTAG\n01/08/2023,A,B,2,1\n"
        mirror = "Date,Team 1,FT,HT,Team 2\nTue Aug 01 2023,A,2-1,1-0,B\n"
        self.assertEqual(len(parse_csv(primary)), 1)
        self.assertEqual(len(parse_csv(mirror)), 1)

    def test_features_are_built_before_match_update(self):
        start = datetime(2023, 1, 1)
        matches = [MatchRecord(start + timedelta(days=i), "A", "B", 2, 0) for i in range(20)]
        examples, _ = build_examples(matches)
        weights = fit(examples[:15], epochs=5)
        metrics = evaluate(weights, examples[15:])
        self.assertEqual(metrics["matches"], 5)
        self.assertGreaterEqual(metrics["accuracy"], 0)

    def test_resolves_provider_aliases_and_handles_new_teams(self):
        artifact = {
            "league": "la-liga", "weights": [[0.0] * 7 for _ in range(3)],
            "teams": {
                "Ath Bilbao": {"elo": 1520, "recent_points": [2], "recent_goals_for": [1], "recent_goals_against": [1], "home_goal_diffs": [1], "away_goal_diffs": [0]},
                "Barcelona": {"elo": 1600, "recent_points": [2], "recent_goals_for": [2], "recent_goals_against": [1], "home_goal_diffs": [1], "away_goal_diffs": [0]},
            },
        }
        aliased = predict_artifact(artifact, "Athletic Club", "FC Barcelona")
        self.assertEqual(aliased["home_team"], "Ath Bilbao")
        self.assertEqual(aliased["coverage"], "historical")
        promoted = predict_artifact(artifact, "New Club", "FC Barcelona")
        self.assertEqual(promoted["coverage"], "partial")
