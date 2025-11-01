from sqlalchemy import Column, Integer, Float, String, UniqueConstraint
from sqlalchemy.orm import declarative_base

base = declarative_base()

class FactGameGenres(base):
    __tablename__ = 'fact_game_genres'
    id = Column(Integer, autoincrement=True, primary_key=True)
    game_id = Column(Integer)
    genre_id = Column(Integer)
    rating = Column(Float)
    rating_count = Column(Integer)
    
class DimGenres(base):
    __tablename__ = 'dim_genres'
    genre_id = Column(Integer, autoincrement=True, primary_key=True)
    genre_name = Column(String, unique=True)

class DimGames(base):
    __tablename__ = 'dim_games'
    game_id = Column(Integer, autoincrement=True, primary_key=True)
    game_name = Column(String, unique=True)
    year_released = Column(Integer)