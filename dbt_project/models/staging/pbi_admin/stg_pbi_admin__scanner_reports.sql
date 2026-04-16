-- stg_pbi_admin__scanner_reports.sql
-- Source: dlt child table scanner_workspaces__reports
-- One row per report returned by the workspace scanner.
-- Join to stg_pbi_admin__scanner_workspaces on _dlt_parent_id = _dlt_id.

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'scanner_workspaces__reports'
) %}

{% if relation %}

select
    _dlt_parent_id                                      as workspace_dlt_id,
    id                                                  as report_id,
    name                                                as report_name,
    report_type,
    dataset_id,
    dataset_workspace_id,
    try_cast(created_date_time as timestamp)            as created_at,
    try_cast(modified_date_time as timestamp)           as modified_at,
    modified_by,
    app_id,
    description,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'scanner_workspaces__reports') }}

{% else %}

select
    null::varchar       as workspace_dlt_id,
    null::varchar       as report_id,
    null::varchar       as report_name,
    null::varchar       as report_type,
    null::varchar       as dataset_id,
    null::varchar       as dataset_workspace_id,
    null::timestamp     as created_at,
    null::timestamp     as modified_at,
    null::varchar       as modified_by,
    null::varchar       as app_id,
    null::varchar       as description,
    null::varchar       as _dlt_load_id,
    null::varchar       as _dlt_id
where 1 = 0

{% endif %}
