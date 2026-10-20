import unittest
from shop.pricing import invoice_total, subtotal, tax


class PricingTest(unittest.TestCase):
    def test_subtotal(self):
        self.assertEqual(subtotal([(2, 500), (1, 250)]), 1250)

    def test_tax_rounds_half_up(self):
        self.assertEqual(tax(1005), 101)

    def test_invoice_total(self):
        self.assertEqual(invoice_total([(2, 500)]), 1100)


if __name__ == "__main__":
    unittest.main()
