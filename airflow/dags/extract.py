from dotenv import load_dotenv
load_dotenv()

from os import getenv
from airflow.sdk import dag, task
from src.etl.extract.rawg_extractor import RAWGExtractor

from datetime import datetime, timedelta

rawg_api_key = getenv('RAWG_API_KEY')
rawg_base_url = getenv('RAWG_BASE_URL')

rawg_extractor = RAWGExtractor(base_url=rawg_base_url)

@dag(dag_id='extract_dag')
def extract_dag():

    @task.python(task_id='request_data')
    def request_data():
        data = rawg_extractor.fetch_data(endpoint="games", params={"ordering": "-rating", "dates": "2020-01-01,2025-12-31",
                                                        "page_size": 10, "key": rawg_api_key})
        print(data)
        return data

    
    @task.python(task_id='save_json_data')
    def save_json_data(rawg_data: dict):
        print(rawg_data)
        rawg_extractor.save_data(rawg_data, f'/opt/airflow/data/raw/{datetime.now().strftime("%Y%m%d")}.json')

    rawg_data = request_data()
    save_json_data(rawg_data)

extract_dag()