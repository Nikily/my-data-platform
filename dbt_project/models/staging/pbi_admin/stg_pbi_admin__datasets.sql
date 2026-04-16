-- stg_pbi_admin__datasets.sql
-- Source: Power BI Admin API — GET /admin/datasets
-- One row per dataset (semantic model) across all workspaces in the tenant.
-- Note: dlt normalises all column names to snake_case.

select
    id                                  as dataset_id,
    name                                as dataset_name,
    configured_by,
    workspace_id,
    is_refreshable,
    is_in_place_sharing_enabled,
    target_storage_mode,
    content_provider_type,
    try_cast(created_date as timestamp) as created_at,
    web_url,
    description,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'datasets') }}
