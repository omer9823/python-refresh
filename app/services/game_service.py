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

    def check_initial_blackjack(self) -> str:
        player_bj = self.player_hand.is_blackjack()
        dealer_bj = self.dealer_hand.is_blackjack()

        if player_bj and dealer_bj:
            return "push"
        if player_bj:
            return "player"
        if dealer_bj:
            return "dealer"
        return "none"
            
    def determine_winner(self) -> str:
            if self.player_hand.is_bust():
                return "dealer"
            if self.dealer_hand.is_bust():
                return "player"
            if self.player_hand.total() > self.dealer_hand.total():
                return "player"
            if self.player_hand.total() < self.dealer_hand.total():
                return "dealer"
            return "push"