def clamp_discount(pct):
    """Discount percent must stay within 0..50 (policy). Negative input once produced a surcharge."""
    return max(0, min(pct, 50))
