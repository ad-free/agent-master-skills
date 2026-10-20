from .shipping import shipping_cost


def label_text(weight_kg):
    return f"Shipping {shipping_cost(weight_kg) / 100:.2f} EUR"
