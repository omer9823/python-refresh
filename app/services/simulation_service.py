from app.services.game_service import GameService
from app.services.advisor_service import AdvisorService

class SimulationService:
    def __init__(self, num_decks: int = 6, penetration: float = 0.75):
        self.num_decks = num_decks
        self.penetration = penetration

    def run_simulation(self, num_hands: int) -> dict:
        results = {"player": 0, "dealer": 0, "push": 0}
        game = GameService(self.num_decks)

        for _ in range(num_hands):
            # Check if penetration limit reached, reshuffle if needed
            if game.shoe.penetration >= self.penetration:
                game = GameService(self.num_decks)

            game.start_game()

            # Check for initial blackjack
            result = game.check_initial_blackjack()
            if result != "none":
                results[result] += 1
                continue

            # Player turn (auto play based on advisor)
            while True:
                advice = AdvisorService.advise_basic(game.player_hand, game.dealer_hand.cards[0].rank)
                if advice == "hit":
                    game.player_hit()
                    if game.player_hand.is_bust():
                        break
                else:
                    break

            # Dealer turn
            game.dealer_play()

            # Determine winner and record result
            winner = game.determine_winner()
            results[winner] += 1

        return results
