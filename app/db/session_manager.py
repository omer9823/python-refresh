from app.db.session import SessionLocal

class DBSessionManager:
    @staticmethod
    def get_session():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
