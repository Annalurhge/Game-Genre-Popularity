import pandas as pd
import numpy as np
import re
import json

class GameBrainTransformer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        with open(self.file_path, 'r') as f:
            self.data = json.load(f)['results']

    def transform(self):
        data = pd.json_normalize(self.data)
        # data = self._remove_na_dates()
        # data = self._remove_duplicates()
        # data = self._standardize_column_names()

        return data

    def _remove_na_dates(self):
        pass

    def _remove_duplicates(self):
        pass

    def _standardize_column_names(self):
        pass