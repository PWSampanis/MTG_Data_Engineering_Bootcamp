Problem description
0 points: Problem is not described
1 point: Problem is described but shortly or not clearly
2 points: Problem is well described and it's clear what the problem the project solves
## What is my problem statement that I want to resolve? Will this data allow me to look
# At aggregate differences between the MTG sets? (would requre full dataset, not oracle
# as oracle only has the newest print of a card... right? )
# Do I want to build a price tracker? If I had streaming data I could watch the prices change for cards
# in real time. 
# I could ask: 
1) Top 10 most expensive cards and their print date
2) Mana curve distributions per set and by color
3) Most reprinted cards (is this all_cards api only or does oracle have any duplicates?)

Cloud
0 points: Cloud is not used, things run only locally
2 points: The project is developed in the cloud
4 points: The project is developed in the cloud and IaC tools are used
## building it on a GCP vm should get me 2 points... need to look into Terraform for 4pts

Data ingestion
Batch / Workflow orchestration
0 points: No workflow orchestration
2 points: Partial workflow orchestration: some steps are orchestrated, some run manually
4 points: End-to-end pipeline: multiple steps in the DAG, uploading data to data lake
## Python script will use pandas to pull the API, normalize the data (or newline delimit it) and then load the data into cloud storage. It could then move it into BQ unless we want to use a dbt external table (would that be a manual process?)

Data warehouse
0 points: No DWH is used
2 points: Tables are created in DWH, but not optimized
4 points: Tables are partitioned and clustered in a way that makes sense for the upstream queries (with explanation)

Transformations (dbt, spark, etc)
0 points: No tranformations
2 points: Simple SQL transformation (no dbt or similar tools)
4 points: Tranformations are defined with dbt, Spark or similar technologies

Dashboard
0 points: No dashboard
2 points: A dashboard with 1 tile
4 points: A dashboard with 2 tiles

Reproducibility
0 points: No instructions how to run code at all
2 points: Some instructions are there, but they are not complete
4 points: Instructions are clear, it's easy to run the code, and the code works