import unittest
from ledger.core import Ledger


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.l = Ledger()
        self.l.open("a", 1000)
        self.l.open("b", 0)

    def test_transfer(self):
        self.l.transfer("a", "b", 300)
        self.assertEqual((self.l.balances["a"], self.l.balances["b"]), (700, 300))

    def test_insufficient(self):
        with self.assertRaises(ValueError):
            self.l.transfer("a", "b", 5000)


if __name__ == "__main__":
    unittest.main()
