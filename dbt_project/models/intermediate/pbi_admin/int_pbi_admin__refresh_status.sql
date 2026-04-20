-- int_pbi_admin__refresh_status.sql
-- Incremental history of refresh attempts per semantic model.
-- One row per (dataset_id, refresh_id) — deduplicated across hourly ingest runs.
-- New rows are added each hour as pbi_admin_refreshes_raw appends to the raw table.
-- To get the latest status per dataset, filter on:
--   QUALIFY ROW_NUMBER() OVER (PARTITION BY dataset_id ORDER BY started_at DESC) = 1

{{ config(
    materialized = 'incremental',
    unique_key   = ['dataset_id', 'refresh_id']
) }}

with source as (

    select * from {{ ref('stg_pbi_admin__dataset_refreshes') }}

    {% if is_incremental() %}
    -- Only process rows from loads we haven't seen yet.
    -- _dlt_load_id is a unix timestamp float stored as varchar — cast for comparison.
    where cast(_dlt_load_id as double) > (
        select coalesce(max(cast(_dlt_load_id as double)), 0) from {{ this }}
    )
    {% endif %}

)

select
    dataset_id,
    refresh_id,
    refresh_type,
    started_at,
    ended_at,
    status,
    error_details,
    to_timestamp(cast(_dlt_load_id as double))  as first_seen_at,
    _dlt_load_id,
    _dlt_id

from source
