from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, func
from app.db.base import Base

class GameDB(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    bet_amount = Column(Float, nullable=False)
    result = Column(String, nullable=False)
    true_count = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
