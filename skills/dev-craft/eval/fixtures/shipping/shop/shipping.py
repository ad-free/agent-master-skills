import math


def shipping_cost(weight_kg):
    """Cents. Currently charged per started kilogram, 450 cents each."""
    return math.ceil(weight_kg) * 450
