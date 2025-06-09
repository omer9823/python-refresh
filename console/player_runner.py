from app.models.player import Player
from app.services.game_service import GameService
from app.services.advisor_service import AdvisorService

def play():
    name = input("Enter your name: ")
    player = Player(name=name)
    game = GameService(num_decks=6)

    while True:
        if player.bankroll <= 0:
            print("You're out of money. Game over!")
            break

        print(player)

        try:
            bet = float(input("Enter your bet: "))
        except ValueError:
            print("Invalid input. Try again.")
            continue

        if not player.place_bet(bet):
            print("Invalid bet amount.")
            continue

        if game.shoe.penetration >= 0.75:
            game = GameService(num_decks=6)

        game.start_game()

        true_count = game.shoe.true_count

        # Check for blackjack
        result = game.check_initial_blackjack()
        if result != "none":
            if result == "player":
                print("BLACKJACK!")
                player.win(bet * 2.5)
            elif result == "push":
                print("PUSH.")
                player.win(bet)
            else:
                print("Dealer has Blackjack.")
            continue

        # Player turn
        while True:
            print(f"Your hand: {[card.rank for card in game.player_hand.cards]} Total: {game.player_hand.total()}")
            print(f"Dealer shows: {game.dealer_hand.cards[0].rank}")
            print(f"True count: {true_count:.2f}")

            basic_advice = AdvisorService.advise_basic(game.player_hand, game.dealer_hand.cards[0].rank)
            count_advice = AdvisorService.advise_with_count(game.player_hand, game.dealer_hand.cards[0].rank, true_count)

            print(f"Basic advice: {basic_advice}")
            print(f"Count-aware advice: {count_advice}")

            move = input("Choose action (hit/stand): ").lower()
            if move == "hit":
                game.player_hit()
                if game.player_hand.is_bust():
                    print("You busted!")
                    break
            elif move == "stand":
                break
            else:
                print("Invalid move.")

        # Dealer turn
        if not game.player_hand.is_bust():
            game.dealer_play()

            print(f"Dealer's hand: {[card.rank for card in game.dealer_hand.cards]} Total: {game.dealer_hand.total()}")

            winner = game.determine_winner()
            if winner == "player":
                print("You win!")
                player.win(bet * 2)
            elif winner == "push":
                print("Push.")
                player.win(bet)
            else:
                print("Dealer wins.")

        cont = input("Continue? (y/n): ").lower()
        if cont != "y":
            break

if __name__ == "__main__":
    play()
