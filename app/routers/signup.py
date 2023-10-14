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
def sign_up(username: Annotated[str, Form()], password: Annotated[str, Form()], email: Annotated[EmailStr, Form()], db: Session=Depends(get_db)) :
    if db.query(models.Subscriber).filter(models.Subscriber.email == email).first() :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    
    if db.query(models.Subscriber).filter(models.Subscriber.username == username).first() :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email address already exists")

    new_user = models.Subscriber(username=username, password=Password().get_password_hash(password), email=email)
    db.add(new_user)
    db.commit()