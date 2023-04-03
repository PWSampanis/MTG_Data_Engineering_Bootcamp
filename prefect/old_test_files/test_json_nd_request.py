import json
import requests 


r = requests.get('https://api.scryfall.com/bulk-data/oracle-cards').json()
"""Send a request to the api to pull bulk data for MTG Cards with Oracle numbers"""

# print(f'Status Code: {r.status_code}')
# print(f"Headers: {r.headers['content-type']}")
# print(f'Output Text: {r.text}')

url = r['download_uri']
print(f'\nDownload URL for the Oracle Cards API: {url}')

file_request = requests.get(url).json()

# print(f'Status Code: {file_request.status_code}')
# print(f"Headers: {file_request.headers['content-type']}")

json_result = [json.dumps(record) for record in file_request]

local_ndjson_file = 'data/ndjson_oracle_card_data.json'
with open(local_ndjson_file, 'w') as f:
    for i in json_result:
        f.write(i+'\n')
