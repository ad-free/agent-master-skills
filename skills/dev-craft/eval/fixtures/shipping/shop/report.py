from .shipping import shipping_cost


def monthly_shipping_revenue(parcels_kg):
    return sum(shipping_cost(w) for w in parcels_kg)
