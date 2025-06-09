from app.services.game_service import GameService
from app.services.advisor_service import AdvisorService

class SimulationService:
    def __init__(self, num_decks: int = 6, penetration: float = 0.75, base_bet: int = 10):
        self.num_decks = num_decks
        self.penetration = penetration
        self.base_bet = base_bet

    def get_bet_amount(self, true_count: float) -> int:
        """
        Dynamic betting logic based on true count.
        """
        if true_count < 1:
            return self.base_bet
        elif true_count >= 4:
            return self.base_bet * 8
        elif true_count >= 3:
            return self.base_bet * 4
        elif true_count >= 2:
            return self.base_bet * 2
        else:
            return self.base_bet

    def run_simulation(self, num_hands: int, strategy: str = "basic") -> dict:
        results = {"player": 0, "dealer": 0, "push": 0}
        total_profit = 0
        game = GameService(self.num_decks)

        for _ in range(num_hands):
            if game.shoe.penetration >= self.penetration:
                game = GameService(self.num_decks)

            game.start_game()

            true_count = game.shoe.true_count
            bet_amount = self.get_bet_amount(true_count)

            result = game.check_initial_blackjack()
            if result != "none":
                if result == "player":
                    total_profit += 1.5 * bet_amount
                elif result == "dealer":
                    total_profit -= bet_amount
                # push = no change
                continue

            while True:
                dealer_upcard = game.dealer_hand.cards[0].rank

                if strategy == "basic":
                    advice = AdvisorService.advise_basic(game.player_hand, dealer_upcard)
                elif strategy == "count":
                    advice = AdvisorService.advise_with_count(game.player_hand, dealer_upcard, true_count)
                else:
                    raise ValueError("Unknown strategy")

                if advice == "hit":
                    game.player_hit()
                    if game.player_hand.is_bust():
                        total_profit -= bet_amount
                        break
                else:
                    break

            if not game.player_hand.is_bust():
                game.dealer_play()
                winner = game.determine_winner()
                if winner == "player":
                    total_profit += bet_amount
                elif winner == "dealer":
                    total_profit -= bet_amount
                # push = no change

            results[winner] += 1

        return {"results": results, "profit": total_profit}
