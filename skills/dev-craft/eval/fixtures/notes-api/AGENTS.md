# notes-api

Gate: `python3 -m unittest discover -s tests`

Error format: domain errors raise `Forbidden`, `NotFound` or `Invalid` from `notes/api.py`; never let another
exception reach `handle` (that is a 500).
