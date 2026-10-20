import unittest
from datetime import date
from reports.dates import last_day_of_month
from reports.rank import newest_first


class ReportsTest(unittest.TestCase):
    def test_last_day(self):
        self.assertEqual(last_day_of_month(date(2024, 2, 10)), date(2024, 2, 29))
        self.assertEqual(last_day_of_month(date(2025, 12, 1)), date(2025, 12, 31))

    def test_newest_first(self):
        rows = [{"date": 1, "n": "a"}, {"date": 2, "n": "b"}, {"date": 2, "n": "c"}]
        self.assertEqual([r["n"] for r in newest_first(rows)], ["b", "c", "a"])


if __name__ == "__main__":
    unittest.main()
