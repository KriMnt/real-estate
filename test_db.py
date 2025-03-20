from backend.app.database import get_db

# Test database connection
def test_connection():
    try:
        db = next(get_db())
        result = db.execute("SELECT 1").fetchone()
        print(f"Database connection successful: {result}")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()