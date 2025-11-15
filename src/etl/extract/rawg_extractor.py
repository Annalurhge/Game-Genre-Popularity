from dotenv import load_dotenv
load_dotenv()

from os import getenv

import requests
import json

from typing import Optional

class RAWGExtractor:
    def __init__(self, base_url: str = None, enable_pagination: bool = False, params: dict = None) -> None:
        self.base_url = base_url
        self.enable_pagination = enable_pagination
        self.params = params

    def _make_request(self) -> Optional[dict]:
        try:
            if self.params:
                response = requests.get(self.base_url, params=self.params)
            else:
                response = requests.get(self.base_url)

            response.raise_for_status()

            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {self.base_url}: {e}")

            return None

    def fetch_data(self) -> Optional[dict]:
        data = self._make_request()
        if data:
            if self.enable_pagination:
                self.params = None
                self.base_url = data['next']
            print("Data fetched successfully")

            return data
        else:
            print("Failed to fetch data.")
            print(data)
    
    def save_data(self, data, file_path) -> None:
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)

            print(f"Data saved to {file_path}")
            
        except IOError as e:
            print(f"Error saving data to {file_path}: {e}")
            raise