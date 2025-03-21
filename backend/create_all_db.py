# create_all_db.py
import os
import sys

# Add parent directory to path so we can import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine
from app.models.property import Property  # Import the Property model
from app.models.property_image import PropertyImage  # Add this line

def create_tables():
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("All tables created successfully!")
        
        # Let's verify by listing the tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tables in database: {tables}")
        
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

if __name__ == "__main__":
    create_tables()