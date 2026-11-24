import unittest

from inv.stock import reserve


class ReserveTest(unittest.TestCase):
    def test_moves_units(self):
        stock = {"A": {"available": 5, "reserved": 0}}
        self.assertEqual(reserve(stock, "A", 2), {"available": 3, "reserved": 2})

    def test_rejects_overdraw(self):
        with self.assertRaises(ValueError):
            reserve({"A": {"available": 1, "reserved": 0}}, "A", 2)


if __name__ == "__main__":
    unittest.main()
