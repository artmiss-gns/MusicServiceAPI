from pydantic import BaseModel
from typing import Optional

class get_Song_response(BaseModel) : # TODO --> GET_Song_response()
    name: str
    artist: str
    album: Optional[str]=None
    length: int
    likes: int=0

class get_Artist_response(BaseModel): # TODO --> GET_Artist_response()
    name: str

class TokenData(BaseModel):
    username: str
    role: str

class Song(BaseModel) :
    song_id: Optional[int]=None # Optional is because this value will be automatically set on database
    album_id: Optional[int]=None
    name: str
    length: int

    class Config:
        orm_mode = True

class Song_artist(BaseModel) :
    song_id: Optional[int]=None
    artist_id: int

class Playlist(BaseModel): 
    playlist_id: Optional[str]=None
    username: str # user's username
    name: str

class Subscriber(BaseModel) :
    username: str
    email: str # TODO : fix the email type as Email
    password: str