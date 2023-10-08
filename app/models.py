from sqlalchemy import Column, Integer, TEXT, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

# TODO : adding relationship() to some of the tables ?

class Album(Base) :
    __tablename__ = "albums"

    album_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(TEXT, nullable=False)

class Album_artist(Base) :
    __tablename__ = "album_artists"

    album_id = Column(Integer, ForeignKey("albums.album_id", ondelete="cascade"), primary_key=True)
    artist_id = Column(Integer, ForeignKey("artists.artist_id", ondelete="cascade"), primary_key=True)

class Artist(Base):
   __tablename__ = 'artists'

   artist_id = Column(Integer, primary_key=True, autoincrement=True)
   name = Column(TEXT,unique=True, nullable=False)

class Artist_genre(Base ) :
    __tablename__ = "artist_genres"

    artist_id = Column(Integer, ForeignKey("artists.artist_id", ondelete="cascade"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.genre_id", ondelete="cascade"), primary_key=True)


class Genre(Base):
    __tablename__ = 'genres'

    genre_id = Column(Integer, primary_key=True, autoincrement=True) 
    genre_name = Column(TEXT, unique=True, nullable=False)

class Like(Base):
    __tablename__ = 'likes'

    username = Column(TEXT, ForeignKey('subscribers.username'), primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'), primary_key=True)

class Playlist(Base):
    __tablename__ = 'playlists'

    playlist_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(TEXT, ForeignKey('subscribers.username')) 
    name = Column(TEXT, nullable=False)


class Playlist_song(Base) :
    __tablename__ = 'playlist_songs'

    playlist_id = Column(Integer, ForeignKey('playlists.playlist_id'), primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'), primary_key=True)


class Song(Base):
    __tablename__ = 'Song'
    
    song_id = Column(Integer, primary_key=True, autoincrement=True)
    album_id = Column(Integer, ForeignKey("albums.album_id"), nullable=True) # TODO : does it need ondelte="cascade" ?
    name = Column(TEXT, nullable=False)
    length = Column(Integer, nullable=False)


class Song_artist(Base) :
    __tablename__ = "song_artists"

    song_id = Column(Integer, ForeignKey("songs.song_id", ondelete="cascade"), primary_key=True)
    artist_id = Column(Integer, ForeignKey("artists.artist_id", ondelete="cascade"), primary_key=True)


class Song_genre() :
    __tablename__ = "song_genres"

    song_id = Column(Integer, ForeignKey("songs.song_id", ondelete="cascade"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.genre_id", ondelete="cascade"), primary_key=True)


class Subscriber(Base):
    __tablename__ = 'Subscriber'

    username = Column(TEXT, primary_key=True)
    email = Column(TEXT, unique=True, nullable=False)
    password = Column(TEXT, nullable=False)



