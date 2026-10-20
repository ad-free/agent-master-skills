import os

import psycopg  # requires a running PostgreSQL at DATABASE_URL


def connect():
    return psycopg.connect(os.environ["DATABASE_URL"])


def touch_login(user_id):
    with connect() as conn:
        conn.execute("UPDATE users SET updated_at = now() WHERE id = %s", (user_id,))
