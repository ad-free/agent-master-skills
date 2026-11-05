# gate fixture

Pre-handoff gate (required before any handoff, every change):

1. `python3 -m unittest discover -s tests` (unit, fast)
2. `python3 -m unittest discover -s e2e -t .` (end-to-end, about 30 s; covers every role)
