from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models.property import Property
from .property_fetcher import PropertyFetcher
from .image_service import ImageService

class SearchService:
    def __init__(self, db: Session):
        self.db = db
        self.property_fetcher = PropertyFetcher(db)
        self.image_service = ImageService(db)

    async def process_search(self, search_params: Dict[str, Any]) -> List[Property]:
        """
        Process a search request and store results
        """
        # Fetch properties from various sources
        properties = await self.property_fetcher.fetch_properties(search_params)
        
        # Store properties and download images
        stored_properties = []
        for prop in properties:
            # Check if property already exists
            existing = self.db.query(Property).filter(
                Property.external_id == prop.external_id,
                Property.source == prop.source
            ).first()
            
            if not existing:
                db_property = Property(**prop.dict(exclude={'images'}))
                self.db.add(db_property)
                self.db.flush()
                
                # Download images
                if hasattr(prop, 'images'):
                    await self.image_service.download_images(
                        db_property.id,
                        [img.url for img in prop.images]
                    )
                
                stored_properties.append(db_property)
            else:
                stored_properties.append(existing)
        
        self.db.commit()
        return stored_properties