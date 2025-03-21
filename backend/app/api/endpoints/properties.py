from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from ...database import get_db
from ...schemas.property import Property, PropertyCreate, PropertyImage
from ...models.property import Property as PropertyModel
from ...services.search_service import SearchService

router = APIRouter()

@router.get("/", response_model=List[Property])
def list_properties(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        # Get properties with eager loading of images
        properties = db.query(PropertyModel).offset(skip).limit(limit).all()
        
        # Manual conversion to handle JSON and relationships
        result = []
        for prop in properties:
            # Handle features JSON conversion if needed
            features = prop.features
            if isinstance(features, str):
                try:
                    features = json.loads(features)
                except:
                    features = {}
            
            # Create dict for property
            prop_dict = {
                "id": prop.id,
                "external_id": prop.external_id,
                "source": prop.source,
                "title": prop.title,
                "description": prop.description,
                "price": prop.price,
                "currency": prop.currency,
                "location": prop.location,
                "area": prop.area,
                "rooms": prop.rooms,
                "features": features,
                "created_at": prop.created_at,
                "updated_at": prop.updated_at,
                "images": []
            }
            
            # Add images if they exist
            if hasattr(prop, 'images'):
                for img in prop.images:
                    prop_dict["images"].append({
                        "id": img.id,
                        "url": img.url,
                        "local_path": img.local_path,
                        "property_id": img.property_id
                    })
            
            result.append(prop_dict)
        
        return result
    except Exception as e:
        print(f"Error getting properties: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{property_id}", response_model=Property)
def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    try:
        property = db.query(PropertyModel).filter(PropertyModel.id == property_id).first()
        if property is None:
            raise HTTPException(status_code=404, detail="Property not found")
            
        # Handle features JSON conversion if needed
        features = property.features
        if isinstance(features, str):
            try:
                features = json.loads(features)
            except:
                features = {}
        
        # Create property dictionary
        prop_dict = {
            "id": property.id,
            "external_id": property.external_id,
            "source": property.source,
            "title": property.title,
            "description": property.description,
            "price": property.price,
            "currency": property.currency,
            "location": property.location,
            "area": property.area,
            "rooms": property.rooms,
            "features": features,
            "created_at": property.created_at,
            "updated_at": property.updated_at,
            "images": []
        }
        
        # Add images if they exist
        if hasattr(property, 'images'):
            for img in property.images:
                prop_dict["images"].append({
                    "id": img.id,
                    "url": img.url,
                    "local_path": img.local_path,
                    "property_id": img.property_id
                })
        
        return prop_dict
    except Exception as e:
        print(f"Error getting property: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=Property)
def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db)
):
    try:
        # Convert features to JSON string if needed
        features = property_data.features
        if not isinstance(features, str):
            features = json.dumps(features)
            
        # Create new property model
        db_property = PropertyModel(
            external_id=property_data.external_id,
            source=property_data.source,
            title=property_data.title,
            description=property_data.description,
            price=property_data.price,
            currency=property_data.currency,
            location=property_data.location,
            area=property_data.area,
            rooms=property_data.rooms,
            features=features
        )
        
        db.add(db_property)
        db.commit()
        db.refresh(db_property)
        
        # Convert back to Pydantic model
        result = {
            "id": db_property.id,
            "external_id": db_property.external_id,
            "source": db_property.source,
            "title": db_property.title,
            "description": db_property.description,
            "price": db_property.price,
            "currency": db_property.currency,
            "location": db_property.location,
            "area": db_property.area,
            "rooms": db_property.rooms,
            "features": property_data.features,  # Use original features dict
            "created_at": db_property.created_at,
            "updated_at": db_property.updated_at,
            "images": []
        }
        
        return result
    except Exception as e:
        print(f"Error creating property: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{property_id}", response_model=Property)
def update_property(
    property_id: int,
    property_data: PropertyCreate,
    db: Session = Depends(get_db)
):
    try:
        property = db.query(PropertyModel).filter(PropertyModel.id == property_id).first()
        if property is None:
            raise HTTPException(status_code=404, detail="Property not found")
            
        # Update property fields
        property.external_id = property_data.external_id
        property.source = property_data.source
        property.title = property_data.title
        property.description = property_data.description
        property.price = property_data.price
        property.currency = property_data.currency
        property.location = property_data.location
        property.area = property_data.area
        property.rooms = property_data.rooms
        
        # Convert features to JSON string if needed
        features = property_data.features
        if not isinstance(features, str):
            features = json.dumps(features)
        property.features = features
        
        db.commit()
        db.refresh(property)
        
        # Convert back to Pydantic model
        result = {
            "id": property.id,
            "external_id": property.external_id,
            "source": property.source,
            "title": property.title,
            "description": property.description,
            "price": property.price,
            "currency": property.currency,
            "location": property.location,
            "area": property.area,
            "rooms": property.rooms,
            "features": property_data.features,  # Use original features dict
            "created_at": property.created_at,
            "updated_at": property.updated_at,
            "images": []
        }
        
        # Add images if they exist
        if hasattr(property, 'images'):
            for img in property.images:
                result["images"].append({
                    "id": img.id,
                    "url": img.url,
                    "local_path": img.local_path,
                    "property_id": img.property_id
                })
                
        return result
    except Exception as e:
        print(f"Error updating property: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{property_id}")
def delete_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    try:
        property = db.query(PropertyModel).filter(PropertyModel.id == property_id).first()
        if property is None:
            raise HTTPException(status_code=404, detail="Property not found")
            
        db.delete(property)
        db.commit()
        
        return {"message": "Property deleted successfully"}
    except Exception as e:
        print(f"Error deleting property: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))