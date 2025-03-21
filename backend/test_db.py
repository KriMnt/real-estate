from app.database import get_db
from sqlalchemy import text

def test_connection():
    try:
        db = next(get_db())
        result = db.execute(text("SELECT 1")).fetchone()
        print(f"Database connection successful: {result}")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        print(f"Error type: {type(e)}")
        return False

if __name__ == "__main__":
    test_connection()