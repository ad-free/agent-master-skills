TAX_PERCENT = 10


def subtotal(lines):
    """lines: list of (quantity, unit_price_cents)."""
    return sum(q * p for q, p in lines)


def tax(taxable_cents):
    return (taxable_cents * TAX_PERCENT + 50) // 100


def invoice_total(lines):
    base = subtotal(lines)
    return base + tax(base)
