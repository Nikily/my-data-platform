-- stg_pbi_admin__scanner_datasets.sql
-- Source: dlt child table scanner_workspaces__datasets
-- One row per dataset returned by the workspace scanner.
-- Join to stg_pbi_admin__scanner_workspaces on _dlt_parent_id = _dlt_id.

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'scanner_workspaces__datasets'
) %}

{% if relation %}

select
    _dlt_parent_id                                  as workspace_dlt_id,
    id                                              as dataset_id,
    name                                            as dataset_name,
    configured_by,
    target_storage_mode,
    content_provider_type,
    try_cast(created_date as timestamp)             as created_at,
    description,
    refresh_schedule__local_time_zone_id    as refresh_schedule_timezone,

    _dlt_id

from {{ source('raw_pbi_admin', 'scanner_workspaces__datasets') }}

{% else %}

select
    null::varchar       as workspace_dlt_id,
    null::varchar       as dataset_id,
    null::varchar       as dataset_name,
    null::varchar       as configured_by,
    null::varchar       as target_storage_mode,
    null::varchar       as content_provider_type,
    null::timestamp     as created_at,
    null::varchar       as description,
    null::varchar       as refresh_schedule_timezone,
    null::varchar       as _dlt_id
where 1 = 0

{% endif %}
