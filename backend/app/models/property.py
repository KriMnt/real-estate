from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)
    source = Column(String)  # Which real estate site this came from
    title = Column(String)
    description = Column(Text)
    price = Column(Float)
    currency = Column(String)
    location = Column(String)
    area = Column(Float)
    rooms = Column(Integer)
    features = Column(JSON)
    images = relationship("PropertyImage", back_populates="property")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PropertyImage(Base):
    __tablename__ = "property_images"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    url = Column(String)
    local_path = Column(String)
    property = relationship("Property", back_populates="images")