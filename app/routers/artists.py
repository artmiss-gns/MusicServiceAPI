from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Form
from app.database import get_db

from sqlalchemy import func, select
from sqlalchemy.orm import Session, aliased

import app.models as models
import app.schemas as schemas

from app.schemas import get_Artist_response
from app.utils import map_data_to_model
from app.auth import get_current_user

from typing import List, Optional, Annotated


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

@router.post("/add_song")
def add_song(song_name:Annotated[str, Form()],
            song_length:Annotated[int, Form()], album_name:Annotated[str, Form()]=None, db:Session = Depends(get_db),
            current_user:models.Artist_registration = Depends(get_current_user)
        ) :
    album = db.query(models.Album).filter(album_name == models.Album.name).first() 
    if album and album_name:
        album_id = album.album_id
    elif not album and album_name : # if album_name is specified, but no album found in the database
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album name not found, create an album first if you haven't created one"
        )
    else : 
        album_id = None

    new_song = schemas.Song(name=song_name, album_id=album_id, length=song_length)
    db.add(models.Song(**new_song.model_dump()))
    song_id =  db.query(func.max(models.Song.song_id)).scalar()
    # ! THIS CAN BE A DATABASE DESIGN FLAW, BUT WHENEVER A NEW SONG IS ADDED, WE SHOULD ADD A ROW TO "Song_artist" TABLE TOO
    song_artist = schemas.Song_artist(song_id=song_id, artist_id=current_user.artist_id)
    db.add(models.Song_artist(**song_artist.model_dump()))

    db.commit()