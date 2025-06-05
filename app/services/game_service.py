from ..models.shoe import Shoe
from ..models.hand import Hand


class GameService:
    def __init__(self, num_decks: int = 6):
        self.shoe = Shoe(num_decks)
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def start_game(self):
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        for _ in range(2):
            self.player_hand.add_card(self.shoe.draw())
            self.dealer_hand.add_card(self.shoe.draw())

    def player_hit(self):
        self.player_hand.add_card(self.shoe.draw())

    def dealer_play(self):
        while self.dealer_hand.total() < 17:
            self.dealer_hand.add_card(self.shoe.draw())
