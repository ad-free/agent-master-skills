# Written by the Test Designer from the brief. Do not edit to fit the implementation.
import unittest
from fmt.price import format_price


class FormatPriceDesignerTest(unittest.TestCase):
    def test_half_up_string(self):
        self.assertEqual(format_price("2.675"), "2.68")

    def test_half_up_float_exact(self):
        self.assertEqual(format_price(0.125), "0.13")

    def test_half_up_small(self):
        self.assertEqual(format_price("1.005"), "1.01")

    def test_whole(self):
        self.assertEqual(format_price(3), "3.00")


if __name__ == "__main__":
    unittest.main()
