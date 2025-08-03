from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.game_service import GameService
from app.services.advisor_service import AdvisorService
from app.models.card import Card
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

@router.websocket("/ws/game")
async def websocket_game(websocket: WebSocket):
    await websocket.accept()
    print(f"[WS] Client connected: {websocket.client}")
    game = GameService()
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
            response = {}
            # Prepare advisor text for all actions except after bust or game end
            def get_advice():
                basic_advice = AdvisorService.advise_basic(game.player_hand, game.dealer_hand.cards[0].rank)
                true_count = game.shoe.true_count if hasattr(game.shoe, 'true_count') else 0
                count_advice = AdvisorService.advise_with_count(game.player_hand, game.dealer_hand.cards[0].rank, true_count)
                return basic_advice, count_advice, true_count
            if action == "start":
                game.start_game()
                bj = game.check_initial_blackjack()
                basic_advice, count_advice, true_count = get_advice()
                response = {
                    "player_hand": hand_to_dict(game.player_hand),
                    "dealer_hand": hand_to_dict(game.dealer_hand),
                    "result": bj,
                    "message": "Game started. Your move!" if bj == "none" else f"Result: {bj}",
                    "basic_advice": basic_advice,
                    "count_advice": count_advice,
                    "true_count": true_count
                }
            elif action == "hit":
                game.player_hit()
                if game.player_hand.is_bust():
                    response = {
                        "player_hand": hand_to_dict(game.player_hand),
                        "dealer_hand": hand_to_dict(game.dealer_hand),
                        "result": "bust",
                        "message": "You busted!",
                        "basic_advice": None,
                        "count_advice": None,
                        "true_count": None
                    }
                else:
                    basic_advice, count_advice, true_count = get_advice()
                    response = {
                        "player_hand": hand_to_dict(game.player_hand),
                        "dealer_hand": hand_to_dict(game.dealer_hand),
                        "result": None,
                        "message": "Hit or Stand?",
                        "basic_advice": basic_advice,
                        "count_advice": count_advice,
                        "true_count": true_count
                    }
            elif action == "stand":
                game.dealer_play()
                winner = game.determine_winner()
                basic_advice, count_advice, true_count = get_advice()
                response = {
                    "player_hand": hand_to_dict(game.player_hand),
                    "dealer_hand": hand_to_dict(game.dealer_hand),
                    "result": winner,
                    "message": f"Result: {winner}",
                    "basic_advice": basic_advice,
                    "count_advice": count_advice,
                    "true_count": true_count
                }
            else:
                response = {"error": "Unknown action"}
            await websocket.send_json(response)
    except WebSocketDisconnect:
        print(f"[WS] Client disconnected: {websocket.client}")
        pass