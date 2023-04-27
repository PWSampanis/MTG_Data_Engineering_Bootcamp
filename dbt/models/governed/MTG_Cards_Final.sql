{{ config(
    materialized='table',
    partition_by={
      "field": "release_date",
      "data_type": "date",
      "granularity": "day"
    }
)}}


with governed_data as (select * from {{ ref("stg_mtg_data") }})

select *
from governed_data
