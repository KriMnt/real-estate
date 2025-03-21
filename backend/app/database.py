# # backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()

# MySQL connection
engine = create_engine(
    "mysql+pymysql://root:Hamster123@localhost/real_estate_db",  # Replace "your_password" with your actual MySQL password
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






























# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from .config import get_settings

# # Temporarily use SQLite for testing
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, 
#     connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()