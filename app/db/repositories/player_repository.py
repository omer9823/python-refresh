from sqlalchemy.orm import Session
from app.db.models.player_model import PlayerDB

class PlayerRepository:
    @staticmethod
    def create_player(db: Session, name: str, bankroll: float = 1000) -> PlayerDB:
        player = PlayerDB(name=name, bankroll=bankroll)
        db.add(player)
        db.commit()
        db.refresh(player)
        return player

    @staticmethod
    def get_player_by_id(db: Session, player_id: int) -> PlayerDB | None:
        return db.query(PlayerDB).filter(PlayerDB.id == player_id).first()

    @staticmethod
    def get_player_by_name(db: Session, name: str) -> PlayerDB | None:
        return db.query(PlayerDB).filter(PlayerDB.name == name).first()

    @staticmethod
    def update_bankroll(db: Session, player: PlayerDB, amount: float):
        player.bankroll = amount
        db.commit()
        db.refresh(player)
