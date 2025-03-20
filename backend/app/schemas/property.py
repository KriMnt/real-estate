from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class PropertyImageBase(BaseModel):
    url: str
    local_path: Optional[str] = None

class PropertyImageCreate(PropertyImageBase):
    pass

class PropertyImage(PropertyImageBase):
    id: int
    property_id: int

    class Config:
        from_attributes = True

class PropertyBase(BaseModel):
    external_id: str
    source: str
    title: str
    description: str
    price: float
    currency: str
    location: str
    area: float
    rooms: int
    features: Dict

class PropertyCreate(PropertyBase):
    pass

class Property(PropertyBase):
    id: int
    images: List[PropertyImage]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True