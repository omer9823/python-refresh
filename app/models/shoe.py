import random
from typing import List
from .card import Card


class Shoe:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
              '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
    count_values = {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
                    '7': 0, '8': 0, '9': 0, '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1}

    def __init__(self, num_decks: int = 6):
        self.total_cards = num_decks * 52
        self.cards = self._create_shoe(num_decks)
        random.shuffle(self.cards)
        self.count = 0  # ספירת קלפים

    def _create_shoe(self, num_decks: int) -> List[Card]:
        return [
            Card(rank=rank, suit=suit, value=self.values[rank], count_value=self.count_values[rank])
            for _ in range(num_decks)
            for suit in self.suits
            for rank in self.ranks
        ]

    def draw(self) -> Card:
        card = self.cards.pop()
        self.count += card.count_value
        return card

    @property
    def penetration(self) -> float:
        return len(self.cards) / self.total_cards

    def needs_shuffle(self) -> bool:
        return self.penetration < 0.2
