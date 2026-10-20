class Ledger:
    def __init__(self):
        self.balances = {}

    def open(self, name, cents=0):
        self.balances[name] = cents

    def transfer(self, src, dst, cents):
        if cents <= 0:
            raise ValueError("amount must be positive")
        if self.balances[src] < cents:
            raise ValueError("insufficient funds")
        self.balances[src] -= cents
        self.balances[dst] += cents
