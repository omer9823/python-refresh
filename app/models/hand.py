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
        total = 0
        ace_count = 0

        for card in self.cards:
            if card.rank == 'A':
                ace_count += 1
                total += 11
            else:
                total += card.value

        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1

        return ace_count > 0
    
    def is_pair(self) -> bool:
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank
