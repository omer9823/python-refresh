class AdvisorService:

    @staticmethod
    def advise_basic(player_hand, dealer_upcard: str) -> str:
        player_total = player_hand.total()
        is_soft = player_hand.is_soft()

        # NOTE: For now, we treat 'A' (Ace) as 10 for basic strategy purposes.
        # In future Advisor versions, Ace should be handled separately according to full Blackjack basic strategy tables.
        dealer_value = int(dealer_upcard) if dealer_upcard.isdigit() else 10

        if is_soft:
            if player_total <= 17:
                return "hit"
            elif player_total == 18:
                return "stand" if dealer_value in [2, 7, 8] else "hit"
            else:
                return "stand"
        else:
            if player_total >= 17:
                return "stand"
            elif 13 <= player_total <= 16 and dealer_value <= 6:
                return "stand"
            elif 13 <= player_total <= 16 and dealer_value >= 7:
                return "hit"
            elif player_total <= 12:
                return "hit"
            else:
                return "hit"

    @staticmethod
    def advise_with_count(player_hand, dealer_upcard: str, count: int) -> str:
        # Start with basic advice
        basic_advice = AdvisorService.advise_basic(player_hand, dealer_upcard)

        player_total = player_hand.total()
        dealer_value = int(dealer_upcard) if dealer_upcard.isdigit() else 10

        # Example simple adjustment based on count:
        if basic_advice == "hit" and count >= 4 and player_total == 16 and dealer_value == 10:
            return "stand"

        return basic_advice