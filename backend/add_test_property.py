from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

# Import your models from setup_database.py
from setup_database import Property

# Database connection
DATABASE_URL = "mysql+pymysql://root:Hamster123@localhost/real_estate_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_test_property():
    db = SessionLocal()
    try:
        # Create test property
        test_property = Property(
            external_id="test123",
            source="test-source",
            title="Test Property",
            description="A beautiful 3-bedroom apartment for testing.",
            price=250000.0,
            currency="EUR",
            location="Test City, Downtown",
            area=120.0,
            rooms=3,
            features=json.dumps({"parking": True, "balcony": True})
        )
        
        # Add to database
        db.add(test_property)
        db.commit()
        db.refresh(test_property)
        
        print(f"Test property created with ID: {test_property.id}")
        return True
    except Exception as e:
        db.rollback()
        print(f"Error adding property: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    add_test_property()