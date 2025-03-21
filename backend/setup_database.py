from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Text, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import os

# Database connection
DATABASE_URL = "mysql+pymysql://root:Hamster123@localhost/real_estate_db"
engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)

# Create declarative base
Base = declarative_base()

# Define models
class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(255), unique=True, index=True)
    source = Column(String(100))
    title = Column(String(255))
    description = Column(Text)
    price = Column(Float)
    currency = Column(String(10))
    location = Column(String(255))
    area = Column(Float)
    rooms = Column(Integer)
    features = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class PropertyImage(Base):
    __tablename__ = "property_images"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    url = Column(String(255))
    local_path = Column(String(255))

# Create all tables
def setup_database():
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("All tables created successfully!")
        
        # Verify tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tables in database: {tables}")
        
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

if __name__ == "__main__":
    setup_database()