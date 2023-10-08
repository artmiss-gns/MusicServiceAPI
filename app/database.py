from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Dependency
# used to connect to the database in the routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a database URL for SQLAlchemy
SQLALCHEMY_DATABASE_URL = f"mysql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}\
@{settings.DATABASE_URL}/{settings.DATABASE_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()