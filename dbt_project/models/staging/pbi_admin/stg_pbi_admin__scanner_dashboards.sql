-- stg_pbi_admin__scanner_dashboards.sql
-- Source: dlt child table scanner_workspaces__dashboards
-- One row per dashboard returned by the workspace scanner.
-- Join to stg_pbi_admin__scanner_workspaces on _dlt_parent_id = _dlt_id.

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'scanner_workspaces__dashboards'
) %}

{% if relation %}

select
    _dlt_parent_id                  as workspace_dlt_id,
    id                              as dashboard_id,
    display_name                    as dashboard_name,
    is_read_only,
    app_id,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'scanner_workspaces__dashboards') }}

{% else %}

select
    null::varchar   as workspace_dlt_id,
    null::varchar   as dashboard_id,
    null::varchar   as dashboard_name,
    null::boolean   as is_read_only,
    null::varchar   as app_id,
    null::varchar   as _dlt_load_id,
    null::varchar   as _dlt_id
where 1 = 0

{% endif %}
