
class Player:
    def __init__(self, name: str, bankroll: float = 1000):
        self.name = name
        self.bankroll = bankroll

    def place_bet(self, amount: float) -> bool:
        if amount > self.bankroll or amount <= 0:
            return False
        self.bankroll -= amount
        return True

    def win(self, amount: float):
        self.bankroll += amount

    def __str__(self):
        return f"Player: {self.name}, Bankroll: {self.bankroll:.2f}"
