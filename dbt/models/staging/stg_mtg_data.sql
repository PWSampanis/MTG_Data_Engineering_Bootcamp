with mtg_raw as (select * from {{ source("mtg_testing", "mtg_data_raw") }})

select
--    `id`,
    name,
    mana_cost,
    cmc,
    type_line,
    oracle_text,
    power,
    toughness,
    loyalty,
    `set`,
    set_name,
    rarity,
    artist,
    collector_number,
    color_identity, 
    IF(REGEXP_CONTAINS(type_line, ".*rtifact*.")=True, type_line,"") as artifact_if_statement

    from mtg_raw

