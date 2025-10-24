import requests

url = "https://api.gamebrain.co/v1/games"

headers = {'x-api-key': "d5b5bee87b8f4fae96611999b2435f77"}

params = {
    "filters": '[{"key":"release_date","values":[{"value":"last_5_years"}]}]',
    "sort": "computed_rating",
    "sort-order": "desc",
    "limit": 10,
    "offset": 0,
}

response = requests.get(url, headers=headers, params=params)

print(response.json())