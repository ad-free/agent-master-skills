def reserve(stock: dict, sku: str, qty: int) -> dict:
    """Move qty units of sku from available to reserved. Raises ValueError if not enough is available."""
    if qty <= 0:
        raise ValueError("qty must be positive")
    item = stock[sku]
    if item["available"] < qty:
        raise ValueError("not enough stock")
    item["available"] -= qty
    item["reserved"] += qty
    return item
