from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Form, Body
from app.database import get_db

from sqlalchemy import func, exists
from sqlalchemy.orm import Session, aliased

import app.models as models
import app.schemas as schemas

from app.schemas import get_Artist_response
from app.utils import map_data_to_model
from app.auth import get_current_user, get_current_artist

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


@router.post("/add_song", status_code=status.HTTP_201_CREATED)
def add_song(song_name:Annotated[str, Form()],
            song_length:Annotated[int, Form()], album_name:Annotated[str, Form()]=None, db:Session = Depends(get_db),
            current_artist:models.Artist_registration = Depends(get_current_artist)
        ) :
    # preventing an artist to add a duplicate song name
    # ! it can be fixed with database 'UniqueConstraint', BUT i dont know how :)
    query = db.query(models.Song)\
        .join(models.Song_artist, models.Song_artist.song_id == models.Song.song_id)\
        .filter(models.Song.name == song_name, models.Song_artist.artist_id == current_artist.artist_id)
    
    if query.first() :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="There is already song with this name for the current user"
        )

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
    db.flush()
    song_id =  db.query(func.max(models.Song.song_id)).scalar()
    # ! THIS CAN BE A DATABASE DESIGN FLAW, BUT WHENEVER A NEW SONG IS ADDED, WE SHOULD ADD A ROW TO "Song_artist" TABLE TOO
    # ! IT CAN BE SOLVED USING A "TRIGGER" IN SQLALCHEMY USING 'events'
    # TODO add Triggers 
    # @event.listens_for(Session, "after_flush")
    # def after_flush(session, flush_context):
    # for obj in session.new:
    #     if isinstance(obj, models.Song) : # and not session.is_modified(obj) ???
    #         new_Song_artist = models.Song_artist(song_id=obj.song_id, artist_id=1)
    #         session.add(new_Song_artist)


    song_artist = schemas.Song_artist(song_id=song_id, artist_id=current_artist.artist_id)
    db.add(models.Song_artist(**song_artist.model_dump()))
    db.commit()


@router.delete("/remove_songs")
def remove_song(
    songs_names:list = Body(),
    current_artist:models.Artist_registration = Depends(get_current_artist),
    db:Session = Depends(get_db)
): 
    '''
    Deletes multiple songs
    the data that is sent must be a json formed list
    '''
    selected_song_info = db.query(models.Song)\
        .join(models.Song_artist, models.Song_artist.song_id == models.Song.song_id)\
        .filter(models.Song.name.in_(songs_names), models.Song_artist.artist_id == current_artist.artist_id).all()
    
    # results = db.query(models.Song).filter(models.Song.name.in_(songs_names)).all()
    songs_id = [result.song_id for result in selected_song_info]

    if len(songs_id) != len(songs_names) :
        # when the artist sends a song name that doesn't exists on the database, this can be sent as a warning too
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Some songs doesn't exists!"
        )
    
    # check if all the given songs belongs to the current user , if not we raise an error
    for song_id in songs_id :
        query = db.query(models.Song_artist).filter(
                    (models.Song_artist.artist_id == current_artist.artist_id), (models.Song_artist.song_id == song_id)
                ) 
        if query.first(): # if the song belongs to the current user
            continue
        else :
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to remove this song"
            )
    
    # in this part we are sure that all songs belongs to the current user 
    query = db.query(models.Song_artist).filter( models.Song_artist.song_id.in_(songs_id))
    for r in query.all() :
        song_id = r.song_id
        artist_id = r.artist_id

        # by only deleting the row from Song table, due to ondelete="cascade" on Song_artist, its equivalent row will be removed
        # so no need to remove it from there too, but pay attention that you should commit or flush the changes so it deletes too
        db.delete( # deleting from Song table
            db.query(models.Song).filter(models.Song.song_id == song_id).first()
        ) 
        db.commit()


@router.post("/add_album", status_code=status.HTTP_201_CREATED)
def add_album(album_name:Annotated[str, Form()], db:Session = Depends(get_db),
            current_artist:models.Artist_registration = Depends(get_current_artist)) :
    # checking if the current user already have an album name 
    query = db.query(models.Album)\
        .join(
            models.Album_artist,
            models.Album.album_id == models.Album_artist.album_id
        )\
        .filter(
            models.Album.name == album_name, models.Album_artist.artist_id == current_artist.artist_id
        )
    if query.first() : # if there is already a album with this name for the current user :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="There is already an album with this name for the current user"
        )
    
    max_album_id = db.query(func.max(models.Album.album_id)).scalar()
    new_album_id = 1 if max_album_id is None else max_album_id+1

    db.add(models.Album(album_id=new_album_id, name=album_name))
    db.add(models.Album_artist(album_id=new_album_id, artist_id=current_artist.artist_id)) # ! again by having a trigger here,
                                                                                           # ! we could prevent adding a row manually
    db.commit()


@router.delete("/remove_album", status_code=status.HTTP_200_OK)
def remove_album(album_name:Annotated[str, Form()], db:Session = Depends(get_db),
        current_artist:models.Artist_registration = Depends(get_current_artist)) :
    
    album = db.query(models.Album)\
        .join(
            models.Album_artist,
            models.Album.album_id == models.Album_artist.album_id
        )\
        .filter(
            models.Album.name == album_name, models.Album_artist.artist_id == current_artist.artist_id
        )\
        .first()

    if album :
        db.delete(album)
        db.commit()
    else :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album Doesn't exists!"
        )