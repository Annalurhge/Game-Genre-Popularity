import requests
import json

from typing import Optional

class RAWGExtractor:
    def __init__(self, base_url) -> None:
        self.base_url = base_url

    def _make_request(self, endpoint, params=None) -> Optional[dict]:
        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")

            return None

    def fetch_data(self, endpoint, params=None) -> Optional[dict]:
        print("Fetching data from RAWG API at endpoint: ", endpoint)

        data = self._make_request(endpoint, params)
        if data:
            print("Data fetched successfully")

            return data
        else:
            print("Failed to fetch data.")

            return None
    
    def save_data(self, data, file_path) -> None:
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)

            print(f"Data saved to {file_path}")
            
        except IOError as e:
            print(f"Error saving data to {file_path}: {e}")