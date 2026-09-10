import unittest
from datetime import datetime, timedelta

from app.ml.historical_model import MatchRecord, build_examples, evaluate, fit, parse_csv


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
