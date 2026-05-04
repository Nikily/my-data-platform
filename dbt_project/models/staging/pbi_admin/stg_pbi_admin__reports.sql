-- stg_pbi_admin__reports.sql
-- Source: Power BI Admin API — GET /admin/reports
-- One row per report across all workspaces in the tenant.
-- Note: dlt normalises all column names to snake_case.

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'reports'
) %}

{% if relation %}

select
    id                                              as report_id,
    name                                            as report_name,
    report_type,
    dataset_id,
    workspace_id,
    app_id,
    description,
    created_by,
    try_cast(created_date_time  as timestamp)       as created_at,
    modified_by,
    try_cast(modified_date_time as timestamp)       as modified_at,
    web_url,
    embed_url,
    format,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'reports') }}

{% else %}

select
    null::varchar   as report_id,
    null::varchar   as report_name,
    null::varchar   as report_type,
    null::varchar   as dataset_id,
    null::varchar   as workspace_id,
    null::varchar   as app_id,
    null::varchar   as description,
    null::varchar   as created_by,
    null::timestamp as created_at,
    null::varchar   as modified_by,
    null::timestamp as modified_at,
    null::varchar   as web_url,
    null::varchar   as embed_url,
    null::varchar   as format,
    null::varchar   as _dlt_load_id,
    null::varchar   as _dlt_id
where 1 = 0

{% endif %}
