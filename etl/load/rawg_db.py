import sqlalchemy
import pandas as pd

class RAWGDB:
    def __init__(self, db_uri: str):
        self.engine = sqlalchemy.create_engine(db_uri)

    def load_to_db(self, data: pd.DataFrame, table_name: str, if_exists: str = 'replace') -> None:
        try:
            data.to_sql(table_name, con=self.engine, if_exists="fail", index=False)
        
        except Exception as e:
            print(f"An error occurred while loading data to the database: {e}")
            raise