from app.database import Base, engine
from app.models.property import Property, PropertyImage

def rebuild_tables():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Tables rebuilt successfully!")

if __name__ == "__main__":
    rebuild_tables()