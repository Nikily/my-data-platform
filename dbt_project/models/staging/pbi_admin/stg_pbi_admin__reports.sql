-- stg_pbi_admin__reports.sql
-- Source: Power BI Admin API — GET /admin/reports
-- One row per report across all workspaces in the tenant.

select
    id                                              as report_id,
    name                                            as report_name,
    "reportType"                                    as report_type,
    "datasetId"                                     as dataset_id,
    "workspaceId"                                   as workspace_id,
    "appId"                                         as app_id,
    description,
    "createdBy"                                     as created_by,
    try_cast("createdDateTime"  as timestamp)       as created_at,
    "modifiedBy"                                    as modified_by,
    try_cast("modifiedDateTime" as timestamp)       as modified_at,
    "webUrl"                                        as web_url,
    "embedUrl"                                      as embed_url,
    format,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'reports') }}
