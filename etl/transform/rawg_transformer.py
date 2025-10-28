import pandas as pd
import numpy as np
import re
import json

class RAWGTransformer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
        self.non_nulls = ['released', 'rating', 'genres']

    def load_data(self) -> None:
        with open(self.file_path, 'r') as f:
            self.data = json.load(f)
    
    def save_data(self, file_path: str) -> None:
        self.data.to_csv(file_path, index=False)

    def transform(self, nested_columns: tuple = ('genres', 'platforms'), column_data_types: dict = {'released': 'datetime64[ns]', 'rating': 'float64', 'ratings_count': 'int64'}) -> pd.DataFrame:
        self.tags = nested_columns
        
        self.data = pd.json_normalize(self.data, record_path='results')
        self.data = self.data[['name', 'released', 'rating', 'ratings_count', 'platforms', 'genres']]
        self.data = self._fix_data_type(column_data_types)
        self.data = self._clean_nested_values()
        self.data = self._remove_null_entries()
        self.data.reset_index(drop=True, inplace=True)

        return self.data
    
    def separate_into_rows(self, columns: list[str]) -> pd.DataFrame:
        """
        Separates entries in a specified column that contain multiple values separated by a comma.
        
        For example, if a game has multiple genres listed in a single cell:
        | name         | genres           |
        |--------------|------------------|
        | Game A       | Action, Adventure|

        The function will transform it into multiple rows:
        | name         | genres    |
        |--------------|-----------|
        | Game A       | Action    |
        | Game A       | Adventure |

        Args:
            columns (list): The column/s to separate into multiple rows.
        """

        for column in columns:
            self.data[column] = self.data[column].str.split(', ')
            self.data = self.data.explode(column).reset_index(drop=True)

        return self.data

    def _remove_null_entries(self):
        for col in self.non_nulls:
            self.data[col] = self.data[col].replace('', np.nan)
            
        self.data.dropna(subset=self.non_nulls, inplace=True)
        self.data.reset_index(drop=True, inplace=True)

        return self.data
    
    def _clean_nested_values(self):
        def _is_eng(tag):
            return not bool(re.search(r'[^\u0000-\u007F]', tag))
        
        def _extract_tags(tags):         
            try:
                return ', '.join([tag['platform']['name'] for tag in tags if _is_eng(tag['platform']['name'])])
            except KeyError:
                return ', '.join([tag['name'] for tag in tags if _is_eng(tag['name'])])
        
        for row in self.tags:
            self.data.loc[:, row] = self.data[row].apply(_extract_tags)

        return self.data
    
    def _fix_data_type(self, columns):
        for key, value in columns.items():
            self.data.loc[:, key] = self.data[key].astype(value)

        return self.data