import json
import requests 
from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from google.cloud import storage, bigquery


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
    path = Path('data/prefect_ndjson_oracle_card_data.json')
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
        to_path = path)
    my_bucket = 'dtc_data_lake_zoomcamp_2023_us' 
    gcs_uri = f"gs://{my_bucket}/{path}"
    return gcs_uri

@task(log_prints=True)
def write_to_bq(gcs_uri):
    # Construct a BigQuery client object.
    client = bigquery.Client()

    table_name='mtg_testing.mtg_data_raw'
    schema = [
        bigquery.SchemaField('id', 'STRING'),
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('mana_cost', 'STRING'),
        bigquery.SchemaField('cmc', 'STRING'),
        bigquery.SchemaField('type_line', 'STRING'),
        bigquery.SchemaField('oracle_text', 'STRING'),
        bigquery.SchemaField('power', 'STRING'),
        bigquery.SchemaField('toughness', 'STRING'),
        bigquery.SchemaField('loyalty', 'STRING'),
        bigquery.SchemaField('set', 'STRING'),
        bigquery.SchemaField('set_name', 'STRING'),
        bigquery.SchemaField('rarity', 'STRING'),
        bigquery.SchemaField('artist', 'STRING'),
        bigquery.SchemaField('collector_number', 'STRING'),
        bigquery.SchemaField('color_identity', 'STRING', mode='REPEATED'),
        bigquery.SchemaField('prices', 'RECORD', fields=[
            bigquery.SchemaField('usd','STRING'),
            bigquery.SchemaField('usd_foil','STRING')]),
        bigquery.SchemaField('image_uris', 'RECORD',fields=[
            bigquery.SchemaField('normal','STRING')]),
        bigquery.SchemaField('keywords', 'STRING', mode='REPEATED'),
        bigquery.SchemaField('released_at', 'STRING'),
    ]

    """Define the BigQuery job configuration"""
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        schema=schema,
        ignore_unknown_values=True,)
    # Load the data from Google Cloud Storage into BigQuery
    uri = f'{gcs_uri}'
    load_job = client.load_table_from_uri(uri, table_name, job_config=job_config)
    load_job.result()


@flow()
def etl_api_to_gcs_to_bq(bulk_data_url):
    """The main ETL function which will automate the string of tasks"""
    file_call = fetch_api_data(bulk_data_url)
    local_file_save = write_local(file_call)
    write_to_cloud_storage = write_to_gcs(local_file_save)
    write_BQ=write_to_bq(write_to_cloud_storage)
    print("We successfully printed the file to GCS and to BigQuery!")

if __name__ == "__main__":
    bulk_data_url = "https://api.scryfall.com/bulk-data/oracle-cards"
    etl_api_to_gcs_to_bq(bulk_data_url)
