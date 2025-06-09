from sqlalchemy.orm import Session
from app.db.models.game_model import GameDB

class GameRepository:
    @staticmethod
    def create_game(db: Session, player_id: int, bet_amount: float, result: str, true_count: float) -> GameDB:
        game = GameDB(
            player_id=player_id,
            bet_amount=bet_amount,
            result=result,
            true_count=true_count
        )
        db.add(game)
        db.commit()
        db.refresh(game)
        return game

    @staticmethod
    def get_games_for_player(db: Session, player_id: int):
        return db.query(GameDB).filter(GameDB.player_id == player_id).all()
