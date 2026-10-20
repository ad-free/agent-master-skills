from .shipping import shipping_cost


def cart_total(items_cents, weight_kg):
    return items_cents + shipping_cost(weight_kg)
