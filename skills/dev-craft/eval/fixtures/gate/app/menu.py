ROLE_PERMISSIONS = {
    "hr": {"employee.view", "approvals.view", "payroll.view"},
    "manager": {"employee.view"},
    "employee": {"self.view"},
}

MENU = [
    ("Dashboard", None),
    ("Employees", "employee.view"),
    ("Approvals", "employee.view"),
    ("Payroll", "payroll.view"),
]


def visible_menu(role):
    perms = ROLE_PERMISSIONS.get(role, set())
    return [label for label, perm in MENU if perm is None or perm in perms]
