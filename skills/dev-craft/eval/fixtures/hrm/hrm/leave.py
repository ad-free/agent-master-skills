from datetime import date

EMPLOYEES = {
    "e1": {"name": "Linh Tran", "start": date(2024, 3, 15), "balance_days": 0.0},
    "e2": {"name": "Omar Haddad", "start": date(2022, 1, 3), "balance_days": 12.0},
}
REQUESTS = []


def request_leave(emp_id, days):
    if days <= 0:
        raise ValueError("days must be positive")
    req = {"id": len(REQUESTS) + 1, "emp": emp_id, "days": days, "status": "pending"}
    REQUESTS.append(req)
    return req
