from app.models.player import Player  # Business Logic
from app.services.game_service import GameService
from app.services.advisor_service import AdvisorService

from app.db.session_manager import DBSessionManager
from app.db.repositories.player_repository import PlayerRepository
from app.db.repositories.game_repository import GameRepository

def deposit_funds(player, db, db_player):
    try:
        amount = float(input("How much would you like to deposit? "))
        if amount <= 0:
            print("Invalid amount.")
            return
        player.bankroll += amount
        PlayerRepository.update_bankroll(db, db_player, player.bankroll)
        print(f"New bankroll: {player.bankroll}")
    except ValueError:
        print("Invalid input.")

def play():
    db_session_generator = DBSessionManager.get_session()
    db = next(db_session_generator)

    name = input("Enter your name: ")
    db_player = PlayerRepository.get_player_by_name(db, name)

    if not db_player:
        print("New player detected.")
        try:
            initial_bankroll = float(input("Enter initial deposit amount: "))
        except ValueError:
            print("Invalid input. Defaulting to 1000.")
            initial_bankroll = 1000
        db_player = PlayerRepository.create_player(db, name, initial_bankroll)
    else:
        print(f"Welcome back, {db_player.name}")

    player = Player(name=db_player.name, bankroll=db_player.bankroll)
    game = GameService(num_decks=6)

    while True:
        print(f"\nCurrent bankroll: {player.bankroll}")

        if player.bankroll <= 0:
            print("You are out of money.")
            choice = input("Would you like to deposit more? (y/n): ").lower()
            if choice == 'y':
                deposit_funds(player, db, db_player)
                continue
            else:
                print("Game over.")
                break

        print("\n--- Menu ---")
        print("1. Play a hand")
        print("2. Deposit funds")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            try:
                bet = float(input("Enter your bet: "))
            except ValueError:
                print("Invalid input.")
                continue

            if not player.place_bet(bet):
                print("Invalid bet.")
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
                    print(f"Your hand: {[card.rank for card in game.player_hand.cards]} | Total: {game.player_hand.total()}")
                    print(f"Dealer shows: {game.dealer_hand.cards[0].rank}")
                    print(f"True count: {true_count:.2f}")

                    basic = AdvisorService.advise_basic(game.player_hand, game.dealer_hand.cards[0].rank)
                    count_based = AdvisorService.advise_with_count(game.player_hand, game.dealer_hand.cards[0].rank, true_count)

                    print(f"Basic strategy: {basic} | Count-aware: {count_based}")
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
                        print("Invalid action.")

                # Dealer turn
                if not game.player_hand.is_bust():
                    game.dealer_play()
                    print(f"Dealer's hand: {[card.rank for card in game.dealer_hand.cards]} | Total: {game.dealer_hand.total()}")

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

            # Update bankroll in DB
            PlayerRepository.update_bankroll(db, db_player, player.bankroll)

            # Log game in DB
            GameRepository.create_game(db, db_player.id, bet, final_result, true_count)

        elif choice == "2":
            deposit_funds(player, db, db_player)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

    db.close()

if __name__ == "__main__":
    play()
