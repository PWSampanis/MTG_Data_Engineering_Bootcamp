import json

# First we will run the requests api request to pull the newest data in
# Is this done by API? 

#Next we will use pandas to read_json (instead of JSON package here I think)

# Next we will use to_json (with orient being ?Records?) to spit out
# a newline delimited version of the file

#Then I test load it into BQ to see how it works


# Explore the structure of the data.
filename = 'data/api_data/oracle-cards-20230321210326.json'
with open(filename,'r') as f:
    oracle_card_data = json.load(f)

result = [json.dumps(record) for record in oracle_card_data]

readable_file = 'data/api_data/ndjson_oracle_card_data.json'
with open(readable_file, 'w') as f:
#    json.dump(oracle_card_data, f, indent=4)
    for i in result:
        f.write(i+'\n')
