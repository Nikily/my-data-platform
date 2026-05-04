-- stg_pbi_admin__dashboards.sql
-- Source: Power BI Admin API — GET /admin/dashboards
-- One row per dashboard across all workspaces in the tenant.
-- Note: dlt normalises all column names to snake_case.

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'dashboards'
) %}

{% if relation %}

select
    id                  as dashboard_id,
    display_name        as dashboard_name,
    is_read_only,
    workspace_id,
    app_id,
    web_url,
    embed_url,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'dashboards') }}

{% else %}

select
    null::varchar  as dashboard_id,
    null::varchar  as dashboard_name,
    null::boolean  as is_read_only,
    null::varchar  as workspace_id,
    null::varchar  as app_id,
    null::varchar  as web_url,
    null::varchar  as embed_url,
    null::varchar  as _dlt_load_id,
    null::varchar  as _dlt_id
where 1 = 0

{% endif %}
