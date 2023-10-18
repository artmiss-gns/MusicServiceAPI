from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db

from sqlalchemy import func, select
from sqlalchemy.orm import Session

import app.models as models
from app.schemas import get_Song_response

from typing import List, Optional

router = APIRouter(
    prefix="/songs",
    tags=["songs"]
)


@router.get("/", response_model=List[get_Song_response])
def get_songs(
        artist_name:Optional[str] =None, album_name:Optional[str] =None, song_name:Optional[str] =None,
        db: Session=Depends(get_db)
    ) :
    ''' 
    This route will return ALL songs as : 
        - artist name
        - song name
        - album (if exists)
        - song length
        - likes
    '''

    columns = [
        models.Song.name.label('song name'),
        models.Artist.name.label('artist'), 
        models.Album.name.label('album'),
        models.Song.length, 
        func.count(models.Likes.song_id).label('likes')
    ]
    query = select(*columns)\
            .select_from(models.Song)\
            .join(models.Song_artist, models.Song_artist.song_id == models.Song.song_id)\
            .join(models.Artist, models.Artist.artist_id == models.Song_artist.artist_id)\
            .join(models.Album_artist, models.Artist.artist_id == models.Album_artist.artist_id, isouter=True)\
            .join(models.Album, models.Album.album_id == models.Song.album_id, isouter=True)\
            .join(models.Likes, models.Likes.song_id == models.Song.song_id)\
            .group_by(models.Song.name, models.Artist.name, models.Album.name, models.Song.length)\
            .order_by(models.Artist.name)\
            .filter(
                (models.Artist.name == artist_name) if artist_name!=None else True,
                (models.Album.name == album_name) if album_name!=None else True,
                (models.Song.name == song_name) if song_name!=None else True
            )

    result = db.execute(query).all()
    # converting to pydantic model 
    result = list(
            map(
                lambda r: get_Song_response(name=r[0], artist=r[1], album=r[2], length=r[3], likes=r[4]),
                result
            )
    )

    return result