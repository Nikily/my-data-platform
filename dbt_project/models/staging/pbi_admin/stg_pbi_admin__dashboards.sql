-- stg_pbi_admin__dashboards.sql
-- Source: Power BI Admin API — GET /admin/dashboards
-- One row per dashboard across all workspaces in the tenant.

select
    id                                      as dashboard_id,
    "displayName"                           as dashboard_name,
    "isReadOnly"                            as is_read_only,
    "workspaceId"                           as workspace_id,
    "appId"                                 as app_id,
    "webUrl"                                as web_url,
    "embedUrl"                              as embed_url,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'dashboards') }}
