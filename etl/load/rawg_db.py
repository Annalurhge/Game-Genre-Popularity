import sqlalchemy
import pandas as pd

class RAWGDB:
    def __init__(self, db_url: str):
        self.engine = sqlalchemy.create_engine(db_url)

    def save_to_db(self, data: pd.DataFrame, table_name: str, if_exists: str = 'replace') -> None:
        data.to_sql(table_name, con=self.engine, if_exists=if_exists, index=False)