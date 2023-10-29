from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.database import get_db
import app.models as models
from app.database import engine

# importing the routes
from app.routers import songs, artists, login, signup, users
# creating the tables // will be removed after implementing Alembic
models.Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()
app.include_router(songs.router) # you can also add the prefix and tags here
app.include_router(artists.router)
app.include_router(login.router)
app.include_router(signup.router)
app.include_router(users.router)


@app.get("/")
def root(db: Session=Depends(get_db)) :
    return "Connected!"
