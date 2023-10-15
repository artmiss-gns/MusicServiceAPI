from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm 

import app.models as models
import app.auth as auth
from app.database import get_db
from app.utils import Password
router = APIRouter(
    prefix="/login",
    tags=["login"]
)


@router.post("/")
def login(db:Session = Depends(get_db), login_info:OAuth2PasswordRequestForm = Depends()) :
    username, password = login_info.username, login_info.password

    # check this with database
    user = db.query(models.Subscriber).filter(models.Subscriber.username == username).first()
    if user and  Password.validate_password(password, user.password): # if user exists and password is correct
        # creating token for the user
        data = {"username": user.username} # the data that is used
        token = auth.create_access_token(data, expiration_time=30)
        return token
    else : # through exception
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials."
        )

