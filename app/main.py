from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.database import get_db
import app.models as models


app = FastAPI()

@app.get("/")
def root(db: Session=Depends(get_db)) :
    return "Connected!"

@app.get("/songs")
def get_songs(db: Session=Depends(get_db)) :
    songs = db.query(models.Song).all()
    return songs

