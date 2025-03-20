from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...schemas.property import Property
from ...models.property import Property as PropertyModel
from ...services.search_service import SearchService

router = APIRouter()

@router.get("/properties/", response_model=List[Property])
async def list_properties(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    properties = db.query(PropertyModel).offset(skip).limit(limit).all()
    return properties

@router.get("/properties/{property_id}", response_model=Property)
async def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    property = db.query(PropertyModel).filter(PropertyModel.id == property_id).first()
    if property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return property