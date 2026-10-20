import unittest
from hrm import leave


class LeaveTest(unittest.TestCase):
    def test_request_is_pending(self):
        self.assertEqual(leave.request_leave("e2", 2)["status"], "pending")

    def test_rejects_zero(self):
        with self.assertRaises(ValueError):
            leave.request_leave("e2", 0)


if __name__ == "__main__":
    unittest.main()
