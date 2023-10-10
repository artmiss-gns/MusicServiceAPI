from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.database import get_db
import app.models as models

# importing the routes
from app.routers import songs

app = FastAPI()
app.include_router(songs.router) # you can also add the prefix and tags here


@app.get("/")
def root(db: Session=Depends(get_db)) :
    return "Connected!"
