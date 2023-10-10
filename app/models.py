from sqlalchemy import Column, Integer, TEXT, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

# TODO : adding relationship() to some of the tables ?

class Album(Base) :
    __tablename__ = "Album" # __tablename__ should be the same name as the database's table name

    album_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(TEXT, nullable=False)

class Album_artist(Base) :
    __tablename__ = "Album_artist"

    album_id = Column(Integer, ForeignKey("Album.album_id", ondelete="cascade"), primary_key=True)
    artist_id = Column(Integer, ForeignKey("Artist.artist_id", ondelete="cascade"), primary_key=True)

class Artist(Base):
   __tablename__ = 'Artist'

   artist_id = Column(Integer, primary_key=True, autoincrement=True)
   name = Column(TEXT,unique=True, nullable=False)

class Artist_genre(Base ) :
    __tablename__ = "Artist_genre"

    artist_id = Column(Integer, ForeignKey("Artist.artist_id", ondelete="cascade"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("Genre.genre_id", ondelete="cascade"), primary_key=True)


class Genre(Base):
    __tablename__ = 'Genre'

    genre_id = Column(Integer, primary_key=True, autoincrement=True) 
    genre_name = Column(TEXT, unique=True, nullable=False)

class Likes(Base):
    __tablename__ = 'Likes'

    username = Column(TEXT, ForeignKey('Subscriber.username'), primary_key=True)
    song_id = Column(Integer, ForeignKey('Song.song_id'), primary_key=True)

class Playlist(Base):
    __tablename__ = 'Playlist'

    playlist_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(TEXT, ForeignKey('Subscriber.username')) 
    name = Column(TEXT, nullable=False)


class Playlist_song(Base) :
    __tablename__ = 'Playlist_song'

    playlist_id = Column(Integer, ForeignKey('Playlist.playlist_id'), primary_key=True)
    song_id = Column(Integer, ForeignKey('Song.song_id'), primary_key=True)


class Song(Base):
    __tablename__ = 'Song'
    
    song_id = Column(Integer, primary_key=True, autoincrement=True)
    album_id = Column(Integer, ForeignKey("Album.album_id"), nullable=True) # TODO : does it need ondelte="cascade" ?
    name = Column(TEXT, nullable=False)
    length = Column(Integer, nullable=False)


class Song_artist(Base) :
    __tablename__ = "Song_artist"

    song_id = Column(Integer, ForeignKey("Song.song_id", ondelete="cascade"), primary_key=True)
    artist_id = Column(Integer, ForeignKey("Artist.artist_id", ondelete="cascade"), primary_key=True)


class Song_genre() :
    __tablename__ = "Song_genre"

    song_id = Column(Integer, ForeignKey("Song.song_id", ondelete="cascade"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("Genre.genre_id", ondelete="cascade"), primary_key=True)


class Subscriber(Base):
    __tablename__ = 'Subscriber'

    username = Column(TEXT, primary_key=True)
    email = Column(TEXT, unique=True, nullable=False)
    password = Column(TEXT, nullable=False)



