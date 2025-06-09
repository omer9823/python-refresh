from app.models.player import Player  # זו מחלקת המשחק שלך (Business Logic)
from app.services.game_service import GameService
from app.services.advisor_service import AdvisorService

from app.db.session_manager import DBSessionManager
from app.db.repositories.player_repository import PlayerRepository
from app.db.repositories.game_repository import GameRepository

def play():
    # Open DB session
    db_session_generator = DBSessionManager.get_session()
    db = next(db_session_generator)

    name = input("Enter your name: ")

    # Check if player exists in DB
    db_player = PlayerRepository.get_player_by_name(db, name)

    if not db_player:
        print("Creating new player...")
        db_player = PlayerRepository.create_player(db, name)
    else:
        print("Welcome back,", db_player.name)

    # Load bankroll from DB
    player = Player(name=db_player.name, bankroll=db_player.bankroll)
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
                final_result = "player"
            elif result == "push":
                print("PUSH.")
                player.win(bet)
                final_result = "push"
            else:
                print("Dealer has Blackjack.")
                final_result = "dealer"
        else:
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
                        final_result = "dealer"
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
                final_result = winner

        # Update bankroll to DB
        PlayerRepository.update_bankroll(db, db_player, player.bankroll)

        # Save game result to DB
        GameRepository.create_game(db, db_player.id, bet, final_result, true_count)

        cont = input("Continue? (y/n): ").lower()
        if cont != "y":
            break

    db.close()

if __name__ == "__main__":
    play()
