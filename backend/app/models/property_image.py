from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class PropertyImage(Base):
    __tablename__ = "property_images"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    url = Column(String(255))  # Added length 255
    local_path = Column(String(255))  # Added length 255
    
    # Optional: Add relationship to Property model
    # property = relationship("Property", back_populates="images")