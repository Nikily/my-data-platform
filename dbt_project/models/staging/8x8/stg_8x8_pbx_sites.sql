-- stg_8x8_pbx_sites.sql
--
-- Staging model for 8x8 PBX sites from the Analytics API.
-- One row per site. Filters out deleted sites.
-- Used in the intermediate layer to attach a site name to each CDR row.

with source as (
    select * from {{ source('raw_eight_x_eight', 'pbx_sites') }}
),

staged as (
    select
        id          as site_id,
        pbx_id,
        name        as site_name
    from source
    where deleted = false or deleted is null
)

select * from staged
