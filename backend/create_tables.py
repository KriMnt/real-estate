from app.database import engine
from app.models.property import Property
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models that should create tables
# Make sure all models inherit from Base
# Property should be imported and should inherit from Base

def create_all_tables():
    try:
        # This will create all tables defined in models
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

if __name__ == "__main__":
    create_all_tables()