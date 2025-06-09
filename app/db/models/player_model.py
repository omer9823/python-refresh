from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.db.base import Base

class PlayerDB(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    bankroll = Column(Float, nullable=False, default=1000)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
