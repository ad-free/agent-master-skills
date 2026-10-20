import unittest
from app import db


class TouchLoginTest(unittest.TestCase):
    def test_touch_login(self):
        db.touch_login(1)


if __name__ == "__main__":
    unittest.main()
