import pandas as pd
import json

# filepath = f"data/api_data"

# with open('data/api_data/oracle-cards-3rows', encoding='utf-8') as inputfile:
#     df = pd.read_json(inputfile)

# df.to_csv('data/api_data/csv.csv', encoding='utf-8', index=False)

filepath = f"data/api_data"

with open('data/api_data/oracle-cards-20230321210326.json', encoding='utf-8') as inputfile:
    data = json.loads(inputfile.read())

df = pd.json_normalize(data)


df.to_csv('data/staging/oracle_cards.csv', encoding='utf-8', index=False)