class Forbidden(Exception):
    status = 403


class NotFound(Exception):
    status = 404


class Invalid(Exception):
    status = 422


NOTES = {
    1: {"id": 1, "owner": "alice", "text": "alice's plan"},
    2: {"id": 2, "owner": "bob", "text": "bob's salary review"},
}


def _parse_id(note_id: str) -> int:
    if not note_id.isdigit():
        raise Invalid("note id must be a positive integer")
    return int(note_id)


def get_note(user: str, note_id: str) -> dict:
    note = NOTES.get(_parse_id(note_id))
    if note is None:
        raise NotFound()
    return note


def update_note(user: str, note_id: str, text: str) -> dict:
    note = get_note(user, note_id)
    if note["owner"] != user:
        raise Forbidden()
    if not text.strip():
        raise Invalid("text must not be empty")
    note["text"] = text
    return note


def handle(fn, *args):
    try:
        return 200, fn(*args)
    except (Forbidden, NotFound, Invalid) as e:
        return e.status, {"error": type(e).__name__}
    except Exception:
        return 500, {"error": "internal"}
