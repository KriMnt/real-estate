from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ...database import get_db
from ...schemas.property import Property
from ...services.search_service import SearchService

router = APIRouter()

@router.post("/search/", response_model=List[Property])
async def search_properties(
    search_params: Dict[str, Any],
    db: Session = Depends(get_db)
):
    search_service = SearchService(db)
    try:
        results = await search_service.process_search(search_params)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))