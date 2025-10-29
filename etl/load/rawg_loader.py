import sqlalchemy
import pandas as pd

class RAWGDB:
    def __init__(self, db_uri: str, dim_games: pd.DataFrame = None, dim_genres: pd.DataFrame = None) -> None:
        self.engine = sqlalchemy.create_engine(db_uri)
        self.dim_games = dim_games
        self.dim_genres = dim_genres

    def load_to_db(self, data: list[pd.DataFrame], table_name: list[str], if_exists: str = 'append') -> None:
        try:
            for data, table in zip(data, table_name):
                if table is None: continue
                data.to_sql(table, con=self.engine, if_exists=if_exists, index=False)

        except Exception as e:
            print(f"An error occurred while loading data to the database: {e}")
            raise