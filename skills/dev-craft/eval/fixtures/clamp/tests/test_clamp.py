import unittest
from disc.clamp import clamp_discount


class ClampTest(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(clamp_discount(10), 10)

    def test_over_cap(self):
        self.assertEqual(clamp_discount(60), 50)


if __name__ == "__main__":
    unittest.main()
