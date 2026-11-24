import unittest

from notes import api


class NotesTest(unittest.TestCase):
    def test_owner_reads_own_note(self):
        self.assertEqual(api.handle(api.get_note, "alice", "1")[0], 200)

    def test_update_by_other_user_is_forbidden(self):
        self.assertEqual(api.handle(api.update_note, "alice", "2", "x")[0], 403)

    def test_bad_id_is_invalid(self):
        self.assertEqual(api.handle(api.get_note, "alice", "abc")[0], 422)


if __name__ == "__main__":
    unittest.main()
