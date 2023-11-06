from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from sqlalchemy import func

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

# subscriber signup
@router.post("/users", status_code=status.HTTP_201_CREATED) # for normal users
def sign_up(username: Annotated[str, Form()], password: Annotated[str, Form()], email: Annotated[EmailStr, Form()],
            db: Session=Depends(get_db)) :
    
    if db.query(models.Subscriber).filter(models.Subscriber.username == username).first() : # duplicate username
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    
    if db.query(models.Subscriber).filter(models.Subscriber.email == email).first() : # duplicate email
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email address already exists")

    new_user = models.Subscriber(username=username, password=Password().get_password_hash(password), email=email)
    db.add(new_user)
    db.commit()

# artist signup
@router.post("/artists", status_code=status.HTTP_201_CREATED)
def sign_up(username: Annotated[str, Form()], password: Annotated[str, Form()], email: Annotated[EmailStr, Form()],
            db: Session=Depends(get_db)) :
    
    if db.query(models.Artist_registration).filter(models.Artist_registration.username == username).first() :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    
    if db.query(models.Artist_registration).filter(models.Artist_registration.email == email).first() :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email address already exists")


    max_id = db.query(func.max(models.Artist.artist_id)).scalar()
    new_id = 1 if max_id is None else (max_id+1)
    new_artist = models.Artist(artist_id=new_id, name=username)
    db.add(new_artist)
    db.commit()
    # ! artist.name can be changed later, for now it is set to it's username

    new_user = models.Artist_registration(artist_id=new_id, username=username, password=Password().get_password_hash(password), email=email) # can be either artist or subscriber
    db.add(new_user) # subscriber or artist
    db.commit()