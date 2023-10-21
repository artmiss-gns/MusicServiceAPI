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
