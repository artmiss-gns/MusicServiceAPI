from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt, ExpiredSignatureError

from app.config import settings
from app.database import get_db
from app.schemas import TokenData
import app.models as models
from datetime import datetime, timedelta

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expiration_time: int | None = None):
    to_encode = data.copy()
    if expiration_time:
        expire = datetime.utcnow() + timedelta(minutes=expiration_time)
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)  # default value of expiration , 30 minutes

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) :
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try :
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("username")
        if username : # the verification is successful
            token_data = TokenData(username=username, role=payload.get('role'))
            return token_data
        else :
            raise create_access_token
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired, Login again")
    except JWTError : # when the given token is wrong)
        raise credentials_exception
    

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    '''
    by receiving the TokenData returns User model
    '''
    token_data = verify_token(token)
    if token_data.role == "artist" :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Artists not allowed, log in as a user!"
        )
    elif token_data.role == "subscriber": # subscriber
        current_user = db.query(models.Subscriber).filter(token_data.username == models.Subscriber.username).first()
    else : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="role not defined!")
    
    if current_user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return current_user


def get_current_artist(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    token_data = verify_token(token)
    if token_data.role == "artist" :
        current_artist = db.query(models.Artist_registration).filter(token_data.username == models.Artist_registration.username).first()
    elif token_data.role == "subscriber": # subscriber
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Subscribers not allowed, log in as a Artist!"
        )
    else : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="role not defined!")
    
    if current_artist is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return current_artist