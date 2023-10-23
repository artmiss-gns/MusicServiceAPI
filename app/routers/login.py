from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

import app.models as models
import app.auth as auth
from app.database import get_db
from app.utils import Password

from typing import Annotated

router = APIRouter(
    prefix="/login",
    tags=["login"]
)


@router.post("/users") # for subscribers
def login(db:Session = Depends(get_db), login_info:OAuth2PasswordRequestForm = Depends()) :
    username, password = login_info.username, login_info.password
    user = db.query(models.Subscriber).filter(models.Subscriber.username == username).first()

    if not user : # user doesn't exists :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        ) 
    if user and  Password.validate_password(password, user.password): # if user exists and password is correct
        # creating token for the user
        data = {
            "username": user.username,
            "role": "subscriber"
        } 
        token = auth.create_access_token(data, expiration_time=30)
        return token
    else : # through exception
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials."
        ) 

@router.post("/artists") # for artists
def login(db:Session = Depends(get_db), login_info:OAuth2PasswordRequestForm = Depends()) :
    username, password = login_info.username, login_info.password
    artist = db.query(models.Artist_registration).filter(models.Artist_registration.username == username).first()

    if not artist : # artist doesn't exists :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        ) 
    if artist and Password.validate_password(password, artist.password): # if artist exists and password is correct
        # creating token for the artist
        data = {
            "username": artist.username,
            "role": "artist"
        } 
        token = auth.create_access_token(data, expiration_time=30)
        return token
    else : # through exception
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials."
        ) 
