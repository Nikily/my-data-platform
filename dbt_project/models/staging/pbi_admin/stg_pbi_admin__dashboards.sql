-- stg_pbi_admin__dashboards.sql
-- Source: Power BI Admin API — GET /admin/dashboards
-- One row per dashboard across all workspaces in the tenant.
-- Note: dlt normalises all column names to snake_case.

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
