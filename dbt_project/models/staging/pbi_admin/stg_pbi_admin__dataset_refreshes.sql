-- stg_pbi_admin__dataset_refreshes.sql
-- Source: Power BI Admin API — GET /admin/datasets/{id}/refreshes
-- Append-only — each hourly run adds a new batch of rows.
-- One row per refresh attempt per dataset (last 5 per dataset per ingest run).
-- Note: dlt normalises all column names to snake_case.

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'dataset_refreshes'
) %}

{% if relation %}

select
    dataset_id,
    id                                          as refresh_id,
    refresh_type,
    request_id,
    try_cast(start_time as timestamp)           as started_at,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'dataset_refreshes') }}

{% else %}

select
    null::varchar       as dataset_id,
    null::varchar       as refresh_id,
    null::varchar       as refresh_type,
    null::varchar       as request_id,
    null::timestamp     as started_at,
    null::varchar       as _dlt_load_id,
    null::varchar       as _dlt_id
where 1 = 0

{% endif %}
