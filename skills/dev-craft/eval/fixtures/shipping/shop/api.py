from .shipping import shipping_cost


def quote(weight_kg):
    return {"weight_kg": weight_kg, "shipping_cents": shipping_cost(weight_kg)}
