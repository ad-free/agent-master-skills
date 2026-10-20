from datetime import date, timedelta


def last_day_of_month(d):
    nxt = d.replace(day=28) + timedelta(days=4)
    return nxt.replace(day=1) - timedelta(days=1)
