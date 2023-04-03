import json
import requests 


r = requests.get('https://api.scryfall.com/bulk-data/oracle-cards')
"""Send a request to the api to pull bulk data for MTG Cards with Oracle numbers"""

print(f'Status Code: {r.status_code}')
print(f"Headers: {r.headers['content-type']}")
print(f'Output Text: {r.text}')

json_response = r.json()

url = json_response['download_uri']
print(f'\nDownload URL for the Oracle Cards API: {url}')

file_request = requests.get(url)

print(f'Status Code: {file_request.status_code}')
print(f"Headers: {file_request.headers['content-type']}")

json_card_data = file_request.json()

json_result = [json.dumps(record) for record in json_card_data]

local_ndjson_file = 'data/ndjson_oracle_card_data.json'
with open(local_ndjson_file, 'w') as f:
    for i in json_result:
        f.write(i+'\n')
