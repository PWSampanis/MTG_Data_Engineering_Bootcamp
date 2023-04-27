## Introduction:
Hello and welcome to my project! The goal of this project is to bring Magic The Gathering card data into BigQuery for analysis. 

The raw data will be accessed via the Scryfall API, an open API which has bulk data available. 
For this project we will be pulling the oracle_cards bulk data file as it attempts to provide the most up to date version of every card printed. 
If a card has been printed in many different editions it will only show up once (unless it is also a token card type).
Information about the bulk data api can be found here: https://scryfall.com/docs/api/bulk-data

## Prerequisites:
Google Cloud Project
Virtual Machine / Working environment (video walkthrough linked below)
Anaconda
dbt cloud account
prefect (installed through pip install requirements.txt)

My suggestion is that you follow this helpful video which will walk you through the creation of a VM. The video will also walk you through installing anaconda which is used here (watch everything up until 16:35 timestamp).
VM creation Video: https://youtu.be/ae-CV2KfoN0


## Initial Setup: 
So at this point I am assuming that you have a working environment with Anaconda 3 installed and initialized. 

Next you will need to copy the project repository to your working environment.

via the command line, you can run:
git clone https://github.com/PWSampanis/MTG_Data_Engineering_Bootcamp.git

I would then use the terminal to go into the MTG_Data_Engineering bootcamp folder.

linux VM command:
cd MTG_Data_Engineering_Bootcamp/

You will now likely want to create a conda environment where you will install the requirements. I have saved my conda environment if you would like to replicate it. 

Anaconda Command:
conda env create -f environment.yml

Alternatively, I have exported my packages in a pip-friendly requirements.txt file if you have python but not anaconda.
Python (not Anaconda) Command:
pip install requirements.txt

The above command (depending on anaconda or pip) should allow you to install the prefect and google packages which we will require.

Personal note: my anaconda version info is as follows...
conda version : 22.11.1
conda-build version : 3.22.0
python version : 3.9.13.final.0


## Pipeline

We have two different ways to run this pipeline. The first option is to run the python file from the terminal. The second method would be to create a prefect deployment and then initiate a run job (the deployment method allows us to schedule the pipeline).

Either way, you will want to make sure you are in your conda environment so you have prefect installed. We will need to set up a couple of Prefect blocks so our code will work.  

Commands:
conda activate zoomcamp (my personal environment)
prefect orion start
- When you start orion it should provide a link to the dashboard (Check out the dashboard at http://##.#.#.#:##)
Use the link to launch the dashboard in your web browser. You will want to create two different blocks in the Prefect Web UI:

Block 1: GCP Credentials named "zoom-gcp-creds" (if you want it to match the existing python code)
For this, you will need to create a GCP service account. Make sure you create a JSON key for the GCP service account and add that private key to the GCP Credentials block. 

Block 2: GCS Bucket named "zoom-gcs" (if you want it to match the existing python code)
You can create a bucket in GCP and add the bucket name into this block. In addition, you can connect the GCP credentials you created in Block 1 so you won't encounter authentication issues. 


I then create a separate terminal (using VSCode) and run:
cd MTG_Data_Engineering_Bootcamp/prefect/ (if you are not already in this sub folder)

You need to register these blocks with Prefect. I beieve the command is:
prefect block register -m prefect_gcp

## Pipeline Option 1: Run Python File (Manual)

Now that the prefect blocks are installed, we want to run the pipeline via the terminal.

To run the python file directly: 
python  MTG_Data_Engineering_Bootcamp/prefect/prefect_deployable_file.py

## Pipeline Option 2: Deploy the Pipeline (Can be Scheduled)
Initially you can try and apply my deployments.yaml file. 

Shortcut - run command to apply my existing yaml file:
prefect deployment apply MTG_Data_Engineering_Bootcamp/prefect/etl_api_to_gcs_to_bq-deployment.yaml 

If that deployment doesn't already exist, you will need to build the deployment. 

To build the deployment: 
- prefect deployment build MTG_Data_Engineering_Bootcamp/prefect/prefect_deployable_file.py:etl_api_to_gcs_to_bq -n "MTG ELT flow"
Note: this will create a yaml file called etl_api_to_gcs_to_bq-deployment.yaml

Open up the newly created yaml file and replace the line:
parameters: {}

With:
parameters: {"bulk_data_url":"https://api.scryfall.com/bulk-data/oracle-cards"}

save the yaml file then run the command:
- prefect deployment apply etl_api_to_gcs_to_bq-deployment.yaml 

Either way, the deployment is now built and has been applied. This will create the deployment in the Prefect web UI, accessible via the url generated when you use the prefect deployment apply command or when you activate orion. 

For a one off deployment test run: Open the deployement tab in the Prefect UI and open up the newly created deployment (MTG ELT flow v2 in this example). You have two choices:

For a one time test run, you can just hit the run button and do a quick run. 

For a scheduled run, select Schedule and input your preferred data refresh shedule. 

Either option will send this job to the default queue for an agent to run (the agent will be created in the next step).

Back in the terminal, run the command:
- prefect agent start --work-queue "default"

This agent will run the pending job that's in the deployments queue. 

## dbt
For this section we will assume that you have already run the prefect_deployable_file.py script either through the command line (python prefect_deployable_file.py) or by setting up a deployment and submitting a job from the Prefect web UI to an active agent for completion. 

This run should have populated a table in BigQuery based on your settings. 
The BQ dataset and table names were assigned in the python script, the default was table_name='mtg_testing.mtg_data_raw'. Note that this is table_name={dataset}.{table} so the BQ dataset is mtg_testing and the table name is mtg_data_raw. 

We are now going to go into dbt cloud and set up a new dbt project. You will select the dbt folder in this project's github repo as a remote repository for dbt. It should have the initialized files already and all of the transformations, allowing you to run the existing pipeline.

In the dbt cloud UI, you can go to the command line and run:
dbt deps

This command will ensure that you have any pre-requisite dbt packages.

Next, from the cloud UI, run:
dbt run

This will build out a staging table called stg_mtg_data and a final table called MTG_Cards_Final. It will require the dataset name to be mtg_testing and the table name as mtg_data raw. If you change these variables you will need to adjust the models/raw/bq_default_sources.yml file accordingly.

## Partitioning Note
The final table, MTG_Cards_Final is partitioned by day on the release_date field. Queries within BQ or in Data Studio can include this as a date filter to significantly reduce computational costs.

## Looker Studio (Reporting):
Next, go to the dashboard at https://lookerstudio.google.com/reporting/2a9df7d2-83ad-4e22-b346-6407bb9e1282
Make a copy of the report. When you do, you will be asked to add a data source. Create a new BigQuery data source and connect it to your final table (you can select to use release_date as a partition). 

I've made some adjustments to the data source which you can replicate if you'd like.
Field changes can be done here in Looker Studio: Resources --> Managed Added Data Sources --> Edit your source

1) Formula field to bring full images into my Data Studio report: add a new Column using the formula "image(normal)". Use this as the dimension for the table on the right side of the first page to get full card images.
2) Change Price  and foil_price columns from text to Currency - USD

You should now have a working dashboard based on ScryFall's MTG API!