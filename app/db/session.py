from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Using SQLite for now
DATABASE_URL = "sqlite:///./blackjack.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
