with mtg_raw as (select * from {{ source("mtg_testing", "mtg_data_raw") }})

select
    `id` as card_id,
    name as card_name,
    mana_cost,
    cmc as converted_mana_cost,
    type_line as card_type,
    oracle_text as card_text,
    `power`,
    toughness,
    loyalty,
    `set`,
    set_name,
    rarity,
    artist,
    collector_number,
    color_identity,
    prices.usd as price,
    prices.usd_foil as foil_price,
    image_uris.normal as image_url,
    coalesce(PARSE_DATE('%F',released_at),'2049-01-01') as release_date,
    if(regexp_contains(type_line, ".*rtifact*.") = true, type_line, "") as is_artifact
from mtg_raw
