from dotenv import load_dotenv
from os import getenv

from etl import RAWGExtractor, RAWGTransformer, RAWGModel
from etl import GameBrainExtractor, GameBrainTransformer
from etl import RAWGDB

from icecream import ic

load_dotenv()
#rawg_api_key = getenv('RAWG_API_KEY')
#gamebrain_api_key = getenv('GAMEBRAIN_API_KEY')

#rawg_base_url = getenv('RAWG_BASE_URL')
#gamebrain_base_url = getenv('GAMEBRAIN_BASE_URL')

db_dialect_driver = getenv("DB_DIALECT_DRIVER")
db_user = getenv("DB_USER")
db_password = getenv("DB_PASSWORD")
db_host = getenv("DB_HOST")
db_port = getenv("DB_PORT")
db_name = getenv("DB_NAME")

db_uri = f"{db_dialect_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

#rawg_extractor = RAWGExtractor(base_url=rawg_base_url)
#gamebrain_extractor = GameBrainExtractor(base_url=gamebrain_base_url)

#rawg_data = rawg_extractor.fetch_data(endpoint="games", params={"ordering": "-rating", "dates": "2020-01-01,2025-12-31",
#                                                                "page_size": 10, "key": rawg_api_key})

#gamebrain_data = gamebrain_extractor.fetch_data(endpoint="games", params={"filters": '[{"key":"release_date", "values":[{"value":"last_5_years"}]}]', "sort": "computed_rating", "sort_order":"desc",
#                                                                          "api-key": gamebrain_api_key, "limit": 10, "offset":0})

#rawg_extractor.save_data(rawg_data, file_path="data/raw/rawg_top_rated_games.json")
#amebrain_extractor.save_data(gamebrain_data, file_path="data/raw/gamebrain_top_rated_games.json")

# gbt = GameBrainTransformer(file_path="data/raw/gamebrain_top_rated_games.json")
# gbt.load_data()

rt = RAWGTransformer(file_path="data/raw/rawg_top_rated_games.json")
rt.load_data()
rt.transform()
rt.separate_into_rows(columns=["genres"])
rt.save_data(file_path="data/transformed/rawg_top_rated_games.csv")

rawg_model = RAWGModel(data=rt.data)

rawg_db = RAWGDB(db_uri=db_uri, dim_games=rawg_model.games, dim_genres=rawg_model.genres, dim_ratings=rawg_model.ratings)
rawg_db.load_to_db(data=[rawg_model.games, rawg_model.genres, rawg_model.ratings], table_name=["dim_games", "dim_genres", "dim_ratings"])