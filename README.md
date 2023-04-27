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

Either way, you will want to make sure you are in your conda environment so you have prefect installed. 

Commands:
conda activate zoomcamp (my personal environment)
prefect orion start
- When you start orion it should provide a link to the dashboard (Check out the dashboard at http://##.#.#.#:##)
Use the link to launch the dashboard. You will want to 

I then create a separate terminal (using VSCode) and run:
cd MTG_Data_Engineering_Bootcamp/prefect/ (if you are not already in this sub folder)



## Pipeline Option 1: Run Python File (Manual)

to be able to use blocks in your code you need to run this from the cli:
- prefect block register -m prefect_gcp

If I do a DBT external table I would need to use the dbt external_tables package. 
- The user would need to run dbt deps to be able to initialize the repo

## Infrastructure setup:



commands I'm running when I restart my vm:
- conda activate zoomcamp (my personal environment)
- prefect orion start
- cd prefect/

To run the python file directly: 
- python prefect_deployable_file.py
*Note: you might need to add in your GCP blocks first and activate them with prefect.....*

To build the deployment: 
- prefect deployment build prefect_deployable_file.py:etl_api_to_gcs_to_bq -n "MTG ELT flow"
Note: this will create a yaml file called etl_api_to_gcs_to_bq-deployment.yaml

Open up the newly created yaml file and replace the line:
parameters: {}

With:
parameters: {"bulk_data_url":"https://api.scryfall.com/bulk-data/oracle-cards"}

save the yaml file then run the command:
- prefect deployment apply etl_api_to_gcs_to_bq-deployment.yaml 

This will create the deployment in the Prefect web UI, accessible via the url generated when you use the prefect deployment apply command or when you activate orion. 

For a one off run: Open the deployement tab in the Prefect UI and open up the newly created deployment (MTG ELT flow v2 in this example). You have two choices:

For a one time run, you can just hit the run button and do a quick run. 

For a scheduled run, select Schedule and input your preferred data refresh shedule. 

Either option will send this job to the default queue for an agent to run (the agent will be created in the next step).

Back in te command line, run the command:
- prefect agent start --work-queue "default"

This agent will run the pending job that's in the deployments queue. 

## Personal note: I've built out the yaml myself so hopefully the end user doesn't need to run the prefect deployment commands... right? 
# Or maybe they just need to run the prefect deployment apply command because the file is already built. Would still have to start agent also

## dbt
For this section we will assume that you have already run the prefect_deployable_file.py script either through the command line (python prefect_deployable_file.py) or by setting up a deployment and submitting a job from the Prefect web UI to an active agent for completion. 

This run should have populated a table in BigQuery based on your settings. 
The BQ dataset and table names were assigned in the python script, default was table_name='mtg_testing.mtg_data_raw'. note that this is table_name={dataset}.{table} so the BQ dataset is mtg_testing and the table name is mtg_data_raw. 

We are now going to go into dbt cloud and set up a new project. You will select the dbt folder in this project's github repo for dbt's folder structure

You can connect dbt to the GitHub dbt folder within this repo so you can pull down all of the transformations I've built. This should allow you to run the models. 

In the dbt cloud UI, you can go to the command line and run:
dbt deps

This command will ensure that you have any pre-requisite dbt packages.

Next, from the cloud UI, run:
dbt run

This will build out a staging table called stg_mtg_data and a final table called MTG_Cards_Final. It will require the dataset name to be mtg_testing and the table name as mtg_data raw. If you change these variables you will need to adjuts the models/raw/bq_default_sources.yml file accordingly.

## Partitioning Note
The final table, MTG_Cards_Final is partitioned by day on the release_date field. Queries within BQ or in Data Studio can include this as a date filter to significantly reduce computational costs.

## Looker Studio (Reporting):
Next, go to the dashboard at .....
Make a copy of the report. When you do, change the Data Source to...
make sure all of the charts are working!
Note: I've made a formula field to bring full images into my Data Studio report. This isn't required but allows for nicer presentation. To create the formula, you do:
..

You should now have a working dashboard based on ScryFall's MTG API!

