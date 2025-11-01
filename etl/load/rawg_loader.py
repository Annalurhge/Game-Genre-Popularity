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
            rating_cache = {}

            for row in data.itertuples():
                if row.name not in game_cache:
                    game_obj = self.session.merge(
                        table_schemas[0](
                            game_name=row.name,
                            year_released=row.released.year
                        )
                    )
                    game_cache[row.name] = game_obj
                
                if row.genres not in genre_cache:
                    genre_obj = self.session.merge(
                        table_schemas[1](
                            genre_name=row.genres
                        )
                    )
                    genre_cache[row.genres] = genre_obj

                self.session.flush()

                fact = table_schemas[2](
                game_id = game_cache[row.name].game_id,
                genre_id = genre_cache[row.genres].genre_id,
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