-- stg_pbi_admin__reports.sql
-- Source: Power BI Admin API — GET /admin/reports
-- One row per report across all workspaces in the tenant.
-- Note: dlt normalises all column names to snake_case.

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
