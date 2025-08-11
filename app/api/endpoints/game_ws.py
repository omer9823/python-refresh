from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.game_service import GameService
from app.services.advisor_service import AdvisorService
from app.models.hand import Hand
import json

router = APIRouter()


def hand_to_dict(hand: Hand):
    return {
        "cards": [card.dict() for card in hand.cards],
        "total": hand.total(),
        "is_blackjack": hand.is_blackjack(),
        "is_bust": hand.is_bust(),
    }


def serialize_state(game: GameService, message: str = "", final_results=None):
    # Build state payload including all hands and controls
    player_hands = [hand_to_dict(h) for h in game.player_hands]
    state = {
        "player_hands": player_hands,
        "active_hand_index": game.active_hand_index,
        "dealer_hand": hand_to_dict(game.dealer_hand),
        "can_split": game.can_split(),
        "can_double": game.can_double(),
        "true_count": getattr(game.shoe, "true_count", 0),
        "message": message,
    }
    # Advisor for active hand (if exists)
    if game.player_hands:
        try:
            dealer_up = game.dealer_hand.cards[0].rank if game.dealer_hand.cards else '?'
            basic_advice = AdvisorService.advise_basic(game.player_hand, dealer_up)
            count_advice = AdvisorService.advise_with_count(game.player_hand, dealer_up, state["true_count"])
            state.update({
                "basic_advice": basic_advice,
                "count_advice": count_advice,
            })
        except Exception:
            pass
    # Final results list if provided (signals round complete)
    if final_results is not None:
        state["final_results"] = final_results
        state["round_over"] = True
    else:
        state["round_over"] = False
    return state


@router.websocket("/ws/game")
async def websocket_game(websocket: WebSocket):
    await websocket.accept()
    print(f"[WS] Client connected: {websocket.client}")
    game = GameService()

    def finish_round_and_respond():
        game.dealer_play()
        winners = game.determine_winners()
        return serialize_state(game, message="Round complete.", final_results=winners)

    try:
        while True:
            data = await websocket.receive_text()
            print(f"[WS] Received message: {data}")
            try:
                msg = json.loads(data)
            except Exception:
                await websocket.send_json({"error": "Invalid JSON"})
                continue
            action = msg.get("action")

            if action == "start":
                game.start_game()
                bj = game.check_initial_blackjack()
                if bj == "none":
                    response = serialize_state(game, message="Game started. Your move!")
                else:
                    # Immediate resolution for natural blackjack cases
                    response = finish_round_and_respond()
            elif action == "hit":
                game.player_hit()
                if game.player_hand.is_bust():
                    # Auto-advance to next hand or finish round
                    if not game.player_stand():
                        response = finish_round_and_respond()
                    else:
                        response = serialize_state(game, message="Bust! Next hand.")
                else:
                    response = serialize_state(game, message="Hit or Stand?")
            elif action == "stand":
                # Move to next hand or finish
                if not game.player_stand():
                    response = finish_round_and_respond()
                else:
                    response = serialize_state(game, message="Next hand.")
            elif action == "split":
                if game.can_split() and game.split_current_hand():
                    response = serialize_state(game, message="Split performed. Play first hand.")
                else:
                    response = serialize_state(game, message="Cannot split this hand.")
            elif action == "double":
                if game.can_double():
                    has_more = game.player_double()
                    if not has_more:
                        response = finish_round_and_respond()
                    else:
                        response = serialize_state(game, message="Doubled. Next hand.")
                else:
                    response = serialize_state(game, message="Cannot double this hand.")
            else:
                response = {"error": "Unknown action"}

            await websocket.send_json(response)
    except WebSocketDisconnect:
        print(f"[WS] Client disconnected: {websocket.client}")
        pass