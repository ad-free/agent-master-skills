# notes-api

Minimal notes service. `handle(fn, *args)` is the HTTP boundary: it maps domain errors to status codes
(403 Forbidden, 404 NotFound, 422 Invalid) and anything else to 500. Note ids arrive as strings from the URL.

Tests: `python3 -m unittest discover -s tests`
