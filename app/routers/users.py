from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Form, Body
from app.database import get_db

from sqlalchemy import func, exists
from sqlalchemy.orm import Session, aliased
from sqlalchemy.exc import IntegrityError

import app.models as models
import app.schemas as schemas

from app.schemas import get_Artist_response
from app.utils import map_data_to_model
from app.auth import get_current_user

from typing import List, Optional, Annotated


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/")
def user_info() :
    return None

@router.get("/playlists")
def user_playlists(db:Session = Depends(get_db), current_user:models.Subscriber = Depends(get_current_user)) :
    playlists = db.query(models.Playlist).filter(models.Playlist.username == current_user.username).all()
    return playlists


@router.post("/playlists", status_code=status.HTTP_201_CREATED)
def add_playlist(playlist_name:Annotated[str, Form()],db:Session = Depends(get_db) , current_user=Depends(get_current_user)) :
    playlist = schemas.Playlist(name=playlist_name, username=current_user.username)
    db.add(models.Playlist(**playlist.model_dump()))
    db.commit()


@router.delete("/playlists", status_code=status.HTTP_200_OK)
def remove_playlist(playlist_name:Annotated[str, Form()], playlist_id:Annotated[str, Form()]=None, db:Session = Depends(get_db),
                current_user=Depends(get_current_user)) :
    playlist = db.query(models.Playlist).filter(models.Playlist.name==playlist_name).all()
    if not playlist :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No playlist found!"
        )
    if len(playlist) > 1 and playlist_id is None :
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Multiple playlists found with the same name. Please provide the playlist ID for deletion.",
        )
    elif len(playlist) > 1 and playlist_id is not None :
        playlist = db.query(models.Playlist).filter(models.Playlist.name==playlist_name, models.Playlist.playlist_id == playlist_id).first()
    else :
        playlist = playlist[0]

    db.delete(playlist)
    db.commit()

@router.post("/playlists/add_song", status_code=status.HTTP_201_CREATED)
def playlist_add_song(
    playlist_name: Annotated[str, Form()],
    song_name: Annotated[str, Form()],
    playlist_id: Annotated[str, Form()] = None,
    song_id: Annotated[int, Form()] = None,
    current_user: models.Subscriber = Depends(get_current_user),
    db:Session = Depends(get_db),
):
    # The user can add duplicate songs to the playlist, this can be changed later

    # checking whether the playlist is valid or not
    playlist = db.query(models.Playlist).filter(models.Playlist.name==playlist_name, models.Playlist.username==current_user.username).all()
    if not playlist :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No playlist found for current user!"
        )
    if len(playlist) > 1 and playlist_id is None :
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Multiple playlists found with the same name. Please provide the playlist ID.",
        )
    elif len(playlist) > 1 and playlist_id is not None :
        playlist = db.query(models.Playlist).filter(models.Playlist.name==playlist_name, models.Playlist.playlist_id == playlist_id).first()
    else :
        playlist = playlist[0]
        
    # checking whether the song that is provided by user is valid or not
    song = db.query(models.Song).filter(models.Song.name == song_name).all()
    if not song :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Song found!"
        )
    if len(song) > 1 and song_id is None :
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Multiple Songs found with the same name. Please provide the Song ID.",
        )
    elif len(song) > 1 and song_id is not None :
        song = db.query(models.Song).filter(models.Song.song_id == song_id).first()
    else :
        song = song[0]

    new_playlist_song = models.Playlist_song(playlist_id=playlist.playlist_id, song_id=song.song_id)
    # we could also check if this song is already in the playlist or not, just like we did it before
    # this is another way to catch the errors while committing to database
    try :
        db.add(new_playlist_song)
        db.commit()
    except IntegrityError as e:
        error_message = str(e.orig)
        if "Duplicate entry" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate entry: This song already exists in the playlist.",
            )
        else :
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Something went wrong!",
            )

# removing a song from a playlist  
@router.delete("/playlists/remove_song", status_code=status.HTTP_201_CREATED)
def playlist_remove_song(
    playlist_name: Annotated[str, Form()],
    song_name: Annotated[str, Form()],
    playlist_id: Annotated[str, Form()] = None,
    song_id: Annotated[int, Form()] = None,
    current_user: models.Subscriber = Depends(get_current_user),
    db:Session = Depends(get_db),
):
    if song_id is None :
        song = db.query(models.Song).filter(models.Song.name == song_name).all()
        if not song : 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No Song found!"
            )
        elif len(song) > 1 : # we have multiple songs with this name
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Multiple Songs found with the same name. Please provide the Song ID.",
            )
        else :
            song_id = song[0].song_id
    
    if playlist_id is None :
        playlist = db.query(models.Playlist).filter(
            models.Playlist.name == playlist_name, models.Playlist.username == current_user.username # the ownership is checked here
        ).all()
        print(playlist)
        if not playlist : 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No playlist found for the user!"
            )
        elif len(playlist) > 1 : # we have multiple songs with this name
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Multiple playlists found with the same name. Please provide the Playlist ID.",
            )
        else :
            playlist_id = playlist[0].playlist_id

    playlist_song = db.query(models.Playlist_song).filter(
        playlist_id==models.Playlist_song.playlist_id, song_id==models.Playlist_song.song_id
    ).first()
    if playlist_song is None :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found in this playlist"
        )
    db.delete(playlist_song)
    db.commit()
