Okay, so is this a good place to start building my project?

First I'll want to test pulling data from the scryfall API with Python. I could try the bulk-data file in either JSON or CSV for an initial test. 

Also I assume I need to make the DE_Zoomcamp_Project a github repo of its own so I can host the whole project publicly. 

Will I need a python instance and requirements.txt in this project folder or use docker to preinstall all the required files?
- I have anaconda installed in a different folder at the same level, is that an issue?


It looks like I'm currently using Anaconda (2 versions... base and zoomcamp). There is also a pyhon 3.8 version available

## Bulk Data:
https://scryfall.com/docs/api/bulk-data/all
so if I use the requests library to pull https://api.scryfall.com/bulk-data I should have 5 gzipped files... 
1)"type": "oracle_cards"
2) "type": "unique_artwork"
3) "type": "default_cards"
4) "type": "all_cards"
5) "type": "rulings"

I could try and load these into Cloud Storage as ndjson files. I would need to unzip them (can be done in jupyter notebooks, should also be possible in python). I would then load them into BQ tables. This whole process would run once a day


When using prefect, you run the command *?prefect orion start?* to start up the web application and see progress of jobs. 

to be able to use blocks in your code you need to run this from the cli:
- prefect block register -m prefect_gcp

If I do a DBT external table I would need to use the dbt external_tables package. 
- The user would need to run dbt deps to be able to initialize the repo

## Infrastructure setup:
- 2 service accounts - dbt and prefect (could you use one for both?)

- GCS bucket creation, bigquery dataset creation (I think dbt external table will build the table). It will all rely on the autodetect schema though unless I build the schema into the dbt external table?


commands I'm running when I restart my vm:
- conda activate zoomcamp (my personal environment)
- prefect orion start
- cd prefect/

To run the python file directly: 
- python prefect_deployable_file.py
*Note: you might need to add in your GCP blocks first and activate them with prefect.....*

To build the deployment: 
- prefect deployment build prefect_deployable_file.py:etl_api_to_gcs_to_bq -n "MTG ELT flow"
Note: this will build a yaml file called