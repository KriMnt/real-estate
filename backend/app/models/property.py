from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text
from sqlalchemy.sql import func  # Make sure this line is present
from app.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

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
    
    # Add relationship to images
    images = relationship("PropertyImage", back_populates="property", cascade="all, delete-orphan")

class PropertyImage(Base):
    __tablename__ = "property_images"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    url = Column(String(255))
    local_path = Column(String(255))
    
    # Add back-reference to property
    property = relationship("Property", back_populates="images")