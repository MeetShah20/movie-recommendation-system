"""Database engine, session factory, and the movie catalog table."""

from sqlalchemy import Column, Float, Integer, String, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import DATABASE_URL

Base = declarative_base()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genres = Column(String, default="")
    year = Column(Integer)
    overview = Column(String, default="")
    tagline = Column(String, default="")
    cast = Column(String, default="")
    director = Column(String, default="")
    producers = Column(String, default="")
    runtime = Column(Integer)
    vote_average = Column(Float)
    vote_count = Column(Integer)
    poster_path = Column(String, default="")
    imdb_id = Column(String, default="")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    movielens_id = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)


class Friendship(Base):
    __tablename__ = "friendships"
    __table_args__ = (UniqueConstraint("owner_id", "friend_kind", "friend_id", name="uq_friendship"),)

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, nullable=False, index=True)
    friend_kind = Column(String, nullable=False)
    friend_id = Column(Integer, nullable=False)


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("user_id", "movie_id", name="uq_like"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    movie_id = Column(Integer, nullable=False, index=True)


class Watchlist(Base):
    __tablename__ = "watchlist"
    __table_args__ = (UniqueConstraint("user_id", "movie_id", name="uq_watchlist"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    movie_id = Column(Integer, nullable=False, index=True)


def init_db():
    """Create the tables if they do not exist yet."""
    Base.metadata.create_all(engine)


def get_db():
    """Yield a database session and close it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
