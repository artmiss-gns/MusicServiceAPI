from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from app.database import get_db

from sqlalchemy import func, select
from sqlalchemy.orm import Session, aliased

import app.models as models
from app.schemas import get_Artist_response
from app.utils import map_data_to_model

from typing import List, Optional


router = APIRouter(
    prefix="/artists",
    tags=["artists"]
)

@router.get("/", response_model=List[get_Artist_response])
def get_artists(db: Session=Depends(get_db), artist_name:Optional[str] =None) -> list:
    """
    to get all the artists, it can also act as an search option for searching a 
    specific artist
    """
    query = db.query(models.Artist.name).filter(
        (models.Artist.name == artist_name) if artist_name!=None else True
    )

    result = query.all()
    result = map_data_to_model(model=get_Artist_response, data=result)
    
    return result

