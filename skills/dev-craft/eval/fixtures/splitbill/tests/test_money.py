import unittest
from bill.money import share


class ShareTest(unittest.TestCase):
    def test_even_split(self):
        self.assertEqual(share(100, 4), 25)

    def test_single_payer(self):
        self.assertEqual(share(999, 1), 999)


if __name__ == "__main__":
    unittest.main()
