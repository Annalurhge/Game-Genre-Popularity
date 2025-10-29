import pandas as pd
import numpy as np

from icecream import ic

class RAWGModel:
    def __init__(self, data: pd.DataFrame):
        self.data = data

        self.games: pd.DataFrame = None
        self.genres: pd.DataFrame = None

        try:
            self.games = self._unique_games()
            self.genres = self._unique_genres()
            
        except Exception as e:
            print(f"An error occurred while modeling data: {e}")
            raise
        
        finally:
            ic(self.games)
            ic(self.genres)

    def _unique_games(self) -> pd.DataFrame:
        unique_games = self.data.loc[self.data['name'].duplicated(keep="first") == False, :]
        new_df: pd.DataFrame = pd.DataFrame()

        new_df['game_name'] = unique_games['name']
        new_df['year_released'] = unique_games['released'].astype('datetime64[ns]').dt.year
        new_df['rating'] = unique_games['rating']
        new_df['ratings_count'] = unique_games['ratings_count']

        return new_df.reset_index(drop=True)
    
    def _unique_genres(self) -> pd.DataFrame:
        unique_genres = self.data.loc[self.data['genres'].duplicated(keep='first') == False, :]
        new_df: pd.DataFrame = pd.DataFrame()

        new_df['genre_name'] = unique_genres['genres']
        return new_df.reset_index(drop=True)