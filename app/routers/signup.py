from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated
from pydantic import EmailStr

import app.models as models
from app.database import get_db

from app.utils import Password

router = APIRouter(
    prefix="/signup",
    tags=["signup"]
)

# TODO we should add Artist signup here later
@router.post("/", status_code=status.HTTP_201_CREATED)
def sign_up(username: Annotated[str, Form()], password: Annotated[str, Form()], email: Annotated[EmailStr, Form()],
             is_artist: Annotated[bool, Form()], db: Session=Depends(get_db)) :
    
    table = models.Artist_registration if is_artist else models.Subscriber
    if db.query(table).filter(table.email == email).first() :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    
    if db.query(table).filter(table.username == username).first() :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email address already exists")

    new_user = table(username=username, password=Password().get_password_hash(password), email=email) # can be either artist or subscriber
    db.add(new_user) 
    db.commit()

    if is_artist : # if this is an artist that is registering, we should also add it's data to Artist table
        artist_id = db.query(models.Artist_registration.artist_id).filter(models.Artist_registration.username == username).first()[0]
        new_artist = models.Artist(artist_id= artist_id, name=username)
        db.add(new_artist)
        db.commit()
        # ! artist.name can be changed later, for now it is set to it's username

