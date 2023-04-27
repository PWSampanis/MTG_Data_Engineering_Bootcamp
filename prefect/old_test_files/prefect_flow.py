import json
import requests 
from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(retries=0,log_prints=True)
def fetch_api_data(bulk_data_url: str):
    """This will make a call to the scryfall API, find the newest file
    and get that file in standard json format"""
    r = requests.get(bulk_data_url)
    print(f"API status code: {r.status_code}")

    json_response = r.json()
    daily_file_url = json_response['download_uri']

    file_request = requests.get(daily_file_url)
    json_card_data = file_request.json()
    return json_card_data

@task(log_prints=True)
def write_local(json_card_data):
    """This will take the json data and write it locally, transforming 
    it into newline-delimited json (BigQuery's json format)"""
    json_result = [json.dumps(record) for record in json_card_data]
    path = Path('prefect/data/prefect_ndjson_oracle_card_data.json')
    with open(path, 'w') as f:
        for i in json_result:
            f.write(i+'\n')
    print("The file has been printed locally in newline-delimited format!")
    return path

@task(log_prints=True)
def write_to_gcs(path):
    """This piece will write the newline-delimited json file to a Google
    Cloud Storage bucket (Data Lake)"""
    gcp_cloud_storage_bucket_block = GcsBucket.load("zoom-gcs")
    gcp_cloud_storage_bucket_block.upload_from_path(
        from_path = f"{path}",
        to_path = path
    )
    return

@flow()
def etl_api_to_gcs_to_bq(bulk_data_url):
    """The main ETL function which will automate the string of tasks"""
    file_call = fetch_api_data(bulk_data_url)
    local_file_save = write_local(file_call)
    write_to_cloud_storage = write_to_gcs(local_file_save)
    print("We successfully printed the file to GCS!")

etl_api_to_gcs_to_bq("https://api.scryfall.com/bulk-data/oracle-cards")