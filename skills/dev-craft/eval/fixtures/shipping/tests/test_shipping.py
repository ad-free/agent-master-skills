import unittest
from shop.shipping import shipping_cost


class ShippingTest(unittest.TestCase):
    def test_one_kg(self):
        self.assertEqual(shipping_cost(1), 450)

    def test_fraction(self):
        self.assertEqual(shipping_cost(1.2), 900)


if __name__ == "__main__":
    unittest.main()
