import time
import unittest

from app.menu import visible_menu

# What each role must reach (product rule). Slow on purpose: stands in for a browser suite.
EXPECTED = {
    "hr": ["Dashboard", "Employees", "Approvals", "Payroll"],
    "manager": ["Dashboard", "Employees", "Approvals"],
    "employee": ["Dashboard"],
}


class RoleJourneyTest(unittest.TestCase):
    def test_every_role_reaches_its_pages(self):
        for role, expected in EXPECTED.items():
            with self.subTest(role=role):
                time.sleep(10)
                self.assertEqual(visible_menu(role), expected)


if __name__ == "__main__":
    unittest.main()
