import pandas as pd
import re
import numpy as np
import json

class RAWGTransformer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
        self.non_nulls = ('released', 'rating', 'genres', 'tags')

    def load_data(self) -> None:
        with open(self.file_path, 'r') as f:
            self.data = json.load(f)
    
    def save_data(self, file_path: str) -> None:
        self.data.to_csv(file_path, index=False)

    def transform(self, nested_columns: tuple = ('genres', 'tags', 'platforms'), column_data_types: dict = {'released': 'datetime64[ns]', 'rating': 'float64', 'ratings_count': 'int64'}) -> pd.DataFrame:
        self.tags = nested_columns
        
        self.data = pd.json_normalize(self.data, record_path='results')
        self.data = self.data[['name', 'released', 'rating', 'ratings_count', 'platforms', 'genres', 'tags']]
        self.data = self._fix_data_type(self.data, column_data_types)
        self.data = self._clean_nested_values(self.data, self.tags)
        self.data.dropna(subset=self.non_nulls, inplace=True)
        self.data.reset_index(drop=True, inplace=True)

        return self.data
    
    def _clean_nested_values(self, data, rows):
        def _is_eng(tag):
            return not bool(re.search(r'[^\u0000-\u007F]', tag))
        
        def _extract_tags(tags):         
            try:
                return ', '.join([tag['platform']['name'] for tag in tags if _is_eng(tag['platform']['name'])])
            except KeyError:
                return ', '.join([tag['name'] for tag in tags if _is_eng(tag['name'])])
        
        for row in rows:
            data.loc[:, row] = data[row].apply(_extract_tags)

        return data
    
    def _fix_data_type(self, data, columns):
        for key, value in columns.items():
            data.loc[:, key] = data[key].astype(value)

        return data