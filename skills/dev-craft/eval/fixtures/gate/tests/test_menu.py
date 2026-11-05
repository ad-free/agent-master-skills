import unittest

from app.menu import visible_menu


class MenuTest(unittest.TestCase):
    def test_hr_sees_everything(self):
        self.assertEqual(visible_menu("hr"), ["Dashboard", "Employees", "Approvals", "Payroll"])


if __name__ == "__main__":
    unittest.main()
