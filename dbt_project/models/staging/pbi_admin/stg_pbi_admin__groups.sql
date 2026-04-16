-- stg_pbi_admin__groups.sql
-- Source: Power BI Admin API — GET /admin/groups
-- One row per workspace (group) in the tenant.
-- Note: dlt normalises all column names to snake_case.

select
    id                                      as group_id,
    name                                    as group_name,
    type                                    as group_type,
    state                                   as group_state,
    description,
    is_read_only,
    is_on_dedicated_capacity,
    capacity_id,
    default_dataset_storage_format,
    has_workspace_level_settings,
    pipeline_id,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'groups') }}
