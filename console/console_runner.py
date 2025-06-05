from app.services.game_service import GameService

def play():
    game = GameService()
    game.start_game()

    while True:
        print("\nYour hand:", [card.rank for card in game.player_hand.cards], "Total:", game.player_hand.total())
        print("Dealer shows:", game.dealer_hand.cards[0].rank)
        print("Current count:", game.shoe.count)
        print("Cards left:", len(game.shoe.cards))

        if game.player_hand.is_blackjack():
            print("Blackjack!")
            break

        if game.player_hand.is_bust():
            print("Bust!")
            break

        move = input("Hit or Stand? ").lower()
        if move == 'hit':
            game.player_hit()
        elif move == 'stand':
            game.dealer_play()
            print("\nDealer's hand:", [card.rank for card in game.dealer_hand.cards], "Total:", game.dealer_hand.total())
            if game.dealer_hand.is_bust() or game.dealer_hand.total() < game.player_hand.total():
                print("You win!")   
            elif game.dealer_hand.total() > game.player_hand.total():
                print("Dealer wins!")
            else:
                print("Push!")
            break
        else:
            print("Invalid move.")

if __name__ == "__main__":
    play()
