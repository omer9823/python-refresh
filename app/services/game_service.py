from ..models.shoe import Shoe
from ..models.hand import Hand
from typing import List


class GameService:
    def __init__(self, num_decks: int = 6, max_hands: int = 4):
        self.shoe = Shoe(num_decks)
        self.dealer_hand = Hand()
        # Manage multiple player hands. active_hand_index points to the current hand.
        self.player_hands: List[Hand] = []
        self.active_hand_index: int = 0
        self.max_hands = max_hands

    @property
    def player_hand(self) -> Hand:
        """Backward-compatible accessor for the current active hand."""
        return self.player_hands[self.active_hand_index]

    def start_game(self):
        self.player_hands = [Hand()]
        self.active_hand_index = 0
        self.dealer_hand = Hand()
        for _ in range(2):
            self.player_hand.add_card(self.shoe.draw())
            self.dealer_hand.add_card(self.shoe.draw())

    def can_split(self) -> bool:
        """Return True if the current hand can be split (pair and split limit not exceeded)."""
        if len(self.player_hands) >= self.max_hands:
            return False
        current = self.player_hand
        return len(current.cards) == 2 and current.cards[0].rank == current.cards[1].rank

    def split_current_hand(self) -> bool:
        """Split the current hand into two hands if allowed. Deals one additional card to each new hand.
        Returns True if split performed, else False.
        """
        if not self.can_split():
            return False
        current = self.player_hand
        # Create two new hands from the pair
        first = Hand()
        second = Hand()
        first.add_card(current.cards[0])
        second.add_card(current.cards[1])
        # Replace current hand with first, insert second right after current index
        self.player_hands[self.active_hand_index] = first
        self.player_hands.insert(self.active_hand_index + 1, second)
        # Deal one card to each split hand (standard rule)
        first.add_card(self.shoe.draw())
        second.add_card(self.shoe.draw())
        return True

    def can_double(self) -> bool:
        """Return True if the current hand can double (exactly two cards)."""
        return len(self.player_hand.cards) == 2

    def player_double(self) -> bool:
        """Perform a double: draw exactly one card and then auto-stand the hand.
        Returns True if there is another hand to play after standing, else False.
        """
        self.player_hand.add_card(self.shoe.draw())
        return self.player_stand()

    def player_hit(self):
        self.player_hand.add_card(self.shoe.draw())

    def player_stand(self) -> bool:
        """Mark current hand as finished by moving to next hand.
        Returns True if there is another hand to play, else False.
        """
        if self.active_hand_index < len(self.player_hands) - 1:
            self.active_hand_index += 1
            return True
        return False

    def dealer_play(self):
        while self.dealer_hand.total() < 17:
            self.dealer_hand.add_card(self.shoe.draw())

    def check_initial_blackjack(self) -> str:
        # Only meaningful at start when there is a single player hand
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
        """Backward-compatible: evaluate the CURRENT active hand only."""
        if self.player_hand.is_bust():
            return "dealer"
        if self.dealer_hand.is_bust():
            return "player"
        if self.player_hand.total() > self.dealer_hand.total():
            return "player"
        if self.player_hand.total() < self.dealer_hand.total():
            return "dealer"
        return "push"

    def determine_winners(self) -> List[str]:
        """Evaluate all player hands against the dealer and return a list of results per hand."""
        results: List[str] = []
        for hand in self.player_hands:
            if hand.is_bust():
                results.append("dealer")
                continue
            if self.dealer_hand.is_bust():
                results.append("player")
                continue
            player_total = hand.total()
            dealer_total = self.dealer_hand.total()
            if player_total > dealer_total:
                results.append("player")
            elif player_total < dealer_total:
                results.append("dealer")
            else:
                results.append("push")
        return results