import unittest
from datetime import datetime, timezone

from app.services.credit_service import MAX_FREE_CREDITS, refreshed_balance


class CreditRefreshTest(unittest.TestCase):
    def test_adds_three_credits_per_elapsed_day(self):
        previous = datetime(2026, 9, 1, tzinfo=timezone.utc)
        now = datetime(2026, 9, 3, tzinfo=timezone.utc)
        balance, refreshed_at = refreshed_balance(5, previous, now)
        self.assertEqual(balance, 11)
        self.assertEqual(refreshed_at, now)

    def test_never_exceeds_free_cap(self):
        previous = datetime(2026, 8, 1, tzinfo=timezone.utc)
        now = datetime(2026, 9, 3, tzinfo=timezone.utc)
        balance, _ = refreshed_balance(19, previous, now)
        self.assertEqual(balance, MAX_FREE_CREDITS)
