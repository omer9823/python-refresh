class AdvisorService:

    @staticmethod
    def advise(player_total: int, dealer_upcard: str) -> str:
        """
        Returns a recommendation for HIT/STAND according to a very basic Basic Strategy
        """
        dealer_value = int(dealer_upcard) if dealer_upcard.isdigit() else 10

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