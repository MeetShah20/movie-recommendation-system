"""Database engine, session factory, and the movie catalog table."""

from sqlalchemy import Column, Integer, String, create_engine
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


def init_db():
    """Create the catalog table if it does not exist yet."""
    Base.metadata.create_all(engine)
