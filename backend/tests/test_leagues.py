import unittest

from app.config.leagues import LEAGUES, get_league
from app.services.league_service import list_leagues


class LeaguesTest(unittest.TestCase):
    def test_required_leagues_are_available(self):
        expected = {"premier-league", "la-liga", "serie-a", "bundesliga", "ligue-1", "champions-league", "liga-mx"}
        self.assertEqual(set(LEAGUES), expected)
        self.assertEqual(len(list_leagues()), 7)

    def test_unknown_league_is_rejected(self):
        with self.assertRaises(ValueError):
            get_league("unknown")
