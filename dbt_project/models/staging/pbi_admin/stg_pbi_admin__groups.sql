-- stg_pbi_admin__groups.sql
-- Source: Power BI Admin API — GET /admin/groups
-- One row per workspace (group) in the tenant.

select
    id                                      as group_id,
    name                                    as group_name,
    type                                    as group_type,
    state                                   as group_state,
    description,
    "isReadOnly"                            as is_read_only,
    "isOnDedicatedCapacity"                 as is_on_dedicated_capacity,
    "capacityId"                            as capacity_id,
    "defaultDatasetStorageFormat"           as default_dataset_storage_format,
    "hasWorkspaceLevelSettings"             as has_workspace_level_settings,
    "pipelineId"                            as pipeline_id,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'groups') }}
