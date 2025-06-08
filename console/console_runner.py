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

    while True:
        print("\nYour hand:", [card.rank for card in game.player_hand.cards], "Total:", game.player_hand.total())
        print("Dealer shows:", game.dealer_hand.cards[0].rank)
        print("Current count:", game.shoe.count)
        print("Cards left:", len(game.shoe.cards))

        if game.player_hand.is_bust():
            print("Bust!")
            break

        advice = AdvisorService.advise(game.player_hand.total(), game.dealer_hand.cards[0].rank)
        print(f"Advisor suggests: {advice.upper()}")

        move = input("Hit or Stand? ").lower()
        if move == 'hit':
            game.player_hit()
        elif move == 'stand':
            game.dealer_play()
            print("\nDealer's hand:", [card.rank for card in game.dealer_hand.cards], "Total:", game.dealer_hand.total())

            winner = game.determine_winner()
            if winner == "player":
                print("You win!")
            elif winner == "dealer":
                print("Dealer wins!")
            else:
                print("Push!")
            break
        else:
            print("Invalid move.")

if __name__ == "__main__":
    play()
