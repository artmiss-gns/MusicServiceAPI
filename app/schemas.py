from pydantic import BaseModel
from typing import Optional

class get_Song_response(BaseModel) :
    name: str
    artist: str
    album: Optional[str]=None
    length: int
    likes: int=0

class get_Artist_response(BaseModel):
    name: str

class TokenData(BaseModel):
    username: str
    
class Album(BaseModel) :
    album_id: int
    name: str

class Album_artist(BaseModel) :
    album_id: int
    artist_id :int

class Artist(BaseModel) :
    artist_id: int
    name: str

class Artist_genre(BaseModel) :
    artist_id: int
    album_id: int

class Genre(BaseModel) :
    genre_id: int
    genre_name: str

class Likes(BaseModel) :
    username: str
    song_id: int

class Playlist(BaseModel) :
    playlist_id: int
    username: str
    name: str

class Playlist_songs(BaseModel) :
    playlist_id: int
    song_id: int

class Song(BaseModel) :
    song_id: int
    album_id: int
    name: str
    length: int

    class Config:
        orm_mode = True

class Song_artist(BaseModel) :
    song_id: int
    artist_id: int

class Song_genre(BaseModel) :
    song_id: int
    genre_id: int

class Subscriber(BaseModel) : 
    username: str
    email: str
    password: str # should be stored the password's hash