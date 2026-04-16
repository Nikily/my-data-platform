-- stg_pbi_admin__scanner_workspaces.sql
-- Source: Power BI Workspace Scanner API — POST /admin/workspaces/getInfo
-- One row per workspace returned by the scanner. Nested artifact arrays are
-- normalised by dlt into sibling tables (scanner_workspaces__reports, etc.).
-- Note: dlt normalises all column names to snake_case.

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'scanner_workspaces'
) %}

{% if relation %}

select
    id                                          as workspace_id,
    name                                        as workspace_name,
    type                                        as workspace_type,
    state                                       as workspace_state,
    is_on_dedicated_capacity,
    capacity_id,
    default_dataset_storage_format,
    description,
    data_retrieval_state,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'scanner_workspaces') }}

{% else %}

select
    null::varchar   as workspace_id,
    null::varchar   as workspace_name,
    null::varchar   as workspace_type,
    null::varchar   as workspace_state,
    null::boolean   as is_on_dedicated_capacity,
    null::varchar   as capacity_id,
    null::varchar   as default_dataset_storage_format,
    null::varchar   as description,
    null::varchar   as data_retrieval_state,
    null::varchar   as _dlt_load_id,
    null::varchar   as _dlt_id
where 1 = 0

{% endif %}
