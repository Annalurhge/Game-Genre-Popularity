import sqlalchemy
from sqlalchemy.orm import sessionmaker
import pandas as pd

class RAWGDB:
    def __init__(self, db_uri: str) -> None:
        self.engine = sqlalchemy.create_engine(db_uri)
        self.session = sessionmaker(bind=self.engine)()

    def load_to_db(self, data: pd.DataFrame, table_schemas: list = []) -> None:
            try:
                game_cache = {}
                genre_cache = {}

                DimGames = table_schemas[0]
                DimGenres = table_schemas[1]
                FactGameGenres = table_schemas[2]

                for row in data.itertuples():
                    if row.name in game_cache:
                        game_obj = game_cache[row.name]
                    else:
                        game_obj = self.session.query(DimGames).filter_by(game_name=row.name).first()
                        
                        if not game_obj:
                            game_obj = DimGames(
                                game_name=row.name,
                                year_released=row.released.year
                            )
                            self.session.add(game_obj)
                            self.session.flush() 
                        
                        game_cache[row.name] = game_obj

                    if row.genres in genre_cache:
                        genre_obj = genre_cache[row.genres]
                    else:
                        genre_obj = self.session.query(DimGenres).filter_by(genre_name=row.genres).first()
                        
                        if not genre_obj:
                            genre_obj = DimGenres(genre_name=row.genres)
                            self.session.add(genre_obj)
                            self.session.flush()
                        
                        genre_cache[row.genres] = genre_obj
                    
                    fact = FactGameGenres(
                        game_id = game_obj.game_id,
                        genre_id = genre_obj.genre_id,
                        rating = row.rating,
                        rating_count = row.ratings_count
                    )
                    self.session.add(fact)
                
                self.session.commit()
                print("Data loaded successfully into the database.")

            except Exception as e:
                print(f"An error occurred while loading data to the database: {e}")
                self.session.rollback()
                raise
            
            finally:
                self.session.close()
                self.engine.dispose()