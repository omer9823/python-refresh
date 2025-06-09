from typing import List
from .card import Card


class Hand:
    def __init__(self):
        self.cards: List[Card] = []

    def add_card(self, card: Card):
        self.cards.append(card)

    def total(self) -> int:
        total = sum(card.value for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == 'A')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def is_blackjack(self) -> bool:
        return self.total() == 21 and len(self.cards) == 2

    def is_bust(self) -> bool:
        return self.total() > 21
    
    def is_soft(self) -> bool:
        total = sum(card.value for card in self.cards)
        return any(card.rank == 'A' for card in self.cards) and total <= 21
    
    def is_pair(self) -> bool:
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank
