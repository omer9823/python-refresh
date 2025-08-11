from app.services.game_service import GameService
from app.services.advisor_service import AdvisorService


def play():
    game = GameService()
    game.start_game()

    result = game.check_initial_blackjack()
    if result != "none":
        if result == "player":
            print("Blackjack! You win!")
        elif result == "dealer":
            print("Dealer has Blackjack. You lose!")
        else:
            print("Both have Blackjack. Push!")
        return

    # Play through all player hands (supporting split)
    while True:
        current_hand = game.player_hand
        hand_index = game.active_hand_index + 1
        total_hands = len(game.player_hands)
        print(f"\nHand {hand_index}/{total_hands} -> Your cards: {[card.rank for card in current_hand.cards]} Total: {current_hand.total()}")
        print("Dealer shows:", game.dealer_hand.cards[0].rank)
        print("Current count:", game.shoe.count)
        print("Cards left:", len(game.shoe.cards))

        if current_hand.is_bust():
            print("Bust!")
            # Move to next hand if exists
            if not game.player_stand():
                break
            else:
                continue

        basic_advice = AdvisorService.advise_basic(current_hand, game.dealer_hand.cards[0].rank)
        true_count = game.shoe.true_count
        count_adjusted_advice = AdvisorService.advise_with_count(
            current_hand, game.dealer_hand.cards[0].rank, true_count)

        print(f"Basic Strategy recommends: {basic_advice.upper()}")
        print(f"Count-Adjusted Strategy recommends: {count_adjusted_advice.upper()}")

        # Build options dynamically
        options = ["hit", "stand"]
        if game.can_split():
            options.append("split")
        if game.can_double():
            options.append("double")
        move = input(f"Choose action ({'/'.join(options)}): ").lower()

        if move == 'hit':
            game.player_hit()
        elif move == 'stand':
            # Move to next hand or finish if none
            if not game.player_stand():
                break
        elif move == 'split' and game.can_split():
            performed = game.split_current_hand()
            if performed:
                print("Hand split! Playing first split hand...")
            else:
                print("Cannot split this hand.")
        elif move == 'double' and game.can_double():
            # Double: draw one card and auto-stand
            has_more = game.player_double()
            print("Doubled. Drew one card and stood.")
            if not has_more:
                break
        else:
            print("Invalid move.")

    # Dealer plays once after all player hands are done
    game.dealer_play()
    print("\nDealer's hand:", [card.rank for card in game.dealer_hand.cards], "Total:", game.dealer_hand.total())

    # Resolve each hand independently against dealer
    results = game.determine_winners()
    for idx, (hand, res) in enumerate(zip(game.player_hands, results), start=1):
        hand_cards = [card.rank for card in hand.cards]
        print(f"Hand {idx}: {hand_cards} Total: {hand.total()} -> ", end="")
        if res == "player":
            print("You win!")
        elif res == "dealer":
            print("Dealer wins!")
        else:
            print("Push!")


if __name__ == "__main__":
    play()
