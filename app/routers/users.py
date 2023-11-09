from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Form, Body
from app.database import get_db

from sqlalchemy import func, exists
from sqlalchemy.orm import Session, aliased

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