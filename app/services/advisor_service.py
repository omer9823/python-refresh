from app.rules.basic_strategy import BASIC_STRATEGY_HARD, BASIC_STRATEGY_SOFT, BASIC_STRATEGY_PAIRS
class AdvisorService:

    @staticmethod
    def advise_basic(player_hand, dealer_upcard: str) -> str:
        player_total = player_hand.total()
        is_soft = player_hand.is_soft()
        is_pair = player_hand.is_pair()

        dealer_value = 11 if dealer_upcard == 'A' else (int(dealer_upcard) if dealer_upcard.isdigit() else 10)

        if is_pair:
            pair_rank = 11 if player_hand.cards[0].rank == 'A' else (int(player_hand.cards[0].rank) if player_hand.cards[0].rank.isdigit() else 10)
            advice = BASIC_STRATEGY_PAIRS.get(pair_rank, {}).get(dealer_value, "hit")
        elif is_soft:
            advice = BASIC_STRATEGY_SOFT.get(player_total, {}).get(dealer_value, "hit")
        else:
            if player_total < 8 or player_total > 17:
                return "stand" if player_total >= 17 else "hit"
            advice = BASIC_STRATEGY_HARD.get(player_total, {}).get(dealer_value, "hit")

        return advice

    @staticmethod
    def advise_with_count(player_hand, dealer_upcard: str, true_count: float) -> str:
        basic_advice = AdvisorService.advise_basic(player_hand, dealer_upcard)

        player_total = player_hand.total()
        dealer_value = 11 if dealer_upcard == 'A' else (int(dealer_upcard) if dealer_upcard.isdigit() else 10)

        if basic_advice == "hit" and true_count >= 4 and player_total == 16 and dealer_value == 10:
            return "stand"

        return basic_advice