-- stg_pbi_admin__groups.sql
-- Source: Power BI Admin API — GET /admin/groups
-- One row per workspace (group) in the tenant.
-- Note: dlt normalises all column names to snake_case.

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'groups'
) %}

{% if relation %}

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

{% else %}

select
    null::varchar  as group_id,
    null::varchar  as group_name,
    null::varchar  as group_type,
    null::varchar  as group_state,
    null::varchar  as description,
    null::boolean  as is_read_only,
    null::boolean  as is_on_dedicated_capacity,
    null::varchar  as capacity_id,
    null::varchar  as default_dataset_storage_format,
    null::boolean  as has_workspace_level_settings,
    null::varchar  as pipeline_id,
    null::varchar  as _dlt_load_id,
    null::varchar  as _dlt_id
where 1 = 0

{% endif %}
