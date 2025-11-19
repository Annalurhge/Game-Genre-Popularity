from datetime import datetime, timedelta
from airflow.sdk import dag, task, Variable

import time
import json

@dag(dag_id='extract_dag',
    schedule='@monthly',
    start_date=datetime(2020, 1, 1),
    catchup=True,
    max_active_runs=1
)
def extract_dag():

    @task.python(task_id='request_data')
    def request_data(data_interval_start: datetime):
        from src.etl import RAWGExtractor

        request_params = json.loads(Variable.get("rawg_parameters"))

        start_str = data_interval_start.strftime("%Y-%m-%d")

        end_date = data_interval_start.end_of('month')
        end_str = end_date.strftime("%Y-%m-%d")
        file_prefix = f"/opt/airflow/data/raw/raw_extract_{end_date.strftime('%Y-%m')}"

        date_param = f"{start_str},{end_str}"
        request_params["dates"] = date_param

        rawg_extractor = RAWGExtractor(base_url="https://api.rawg.io/api/games", enable_pagination=True, params=request_params)

        page = 1

        while rawg_extractor.base_url:
            print(f"Fetching from url: {rawg_extractor.base_url}")
            data = rawg_extractor.fetch_data()

            if not data:
                print("No data returned, stopping pagination.")
                break

            rawg_extractor.save_data(data, f'{file_prefix}_page_{page}.json')
            page += 1
            time.sleep(0.21)
    
    @task.python(task_id='clean_data')
    def transform_data(data_interval_start: datetime):
        from src.etl import RAWGTransformer
        import glob

        file_prefix = f"/opt/airflow/data/raw/raw_extract_{data_interval_start.strftime('%Y-%m')}"
        raw_files = glob.glob(f"{file_prefix}_page_*.json")

        for file in raw_files:
            print("Processing file:", file)
            rawg_transformer = RAWGTransformer(file_path=file)
            rawg_transformer.load_data()
            rawg_transformer.transform()
            rawg_transformer.separate_into_rows(columns=["genres"])
            rawg_transformer.save_data(file_path=file.replace("raw", "transformed").replace(".json", ".csv"))


    @task.python(task_id='load_data')
    def load_data(data_interval_start: datetime):
        from src.etl import RAWGDB
        from src.setup_files.database_schema import DimGames, DimGenres, FactGameGenres
        import glob
        import pandas as pd

        db_cred = json.loads(Variable.get("db_creds"))

        db_dialect_driver = db_cred["dialect_driver"]
        db_user = db_cred["user"]
        db_password = db_cred["password"]
        db_host = db_cred["host"]
        db_port = db_cred["port"]
        db_name = db_cred["db_name"]

        db_uri = f"{db_dialect_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        file_prefix = f"/opt/airflow/data/raw/raw_extract_{data_interval_start.strftime('%Y-%m')}"
        transformed_files = glob.glob(f"/opt/airflow/data/transformed/transformed_extract_{data_interval_start.strftime('%Y-%m')}_page_*.csv")

        rawg_db = RAWGDB(db_uri=db_uri)

        for file in transformed_files:
            print("Loading file:", file)
            data = pd.read_csv(file)
            data['released'] = pd.to_datetime(data['released'], errors='coerce')
            rawg_db.load_to_db(data=data, table_schemas=[DimGames, DimGenres, FactGameGenres])


    request_data() >> transform_data() >> load_data()

extract_dag()