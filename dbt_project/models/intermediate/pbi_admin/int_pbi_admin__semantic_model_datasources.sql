-- int_pbi_admin__semantic_model_datasources.sql
-- Semantic models joined to their data sources.
-- One row per (semantic model, datasource) pair.
-- A model using 2 Excel files + 1 Dataverse connection produces 3 rows.

{% set times_relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'scanner_workspaces__datasets__refresh_schedule__times'
) %}

with datasets as (
    select * from {{ ref('stg_pbi_admin__scanner_datasets') }}
),

workspaces as (
    select * from {{ ref('stg_pbi_admin__scanner_workspaces') }}
),

datasource_usages as (
    select * from {{ ref('stg_pbi_admin__scanner_datasets__datasource_usages') }}
),

datasource_instances as (
    select * from {{ ref('stg_pbi_admin__scanner_datasource_instances') }}
),

{% if times_relation %}
refresh_times as (
    -- Aggregate all scheduled times into a single formatted string per dataset.
    -- dlt stores times as "HH:MM" strings in the child table; we format to
    -- "hh:mm am/pm" and join them in scheduled order.
    select
        _dlt_parent_id                  as dataset_dlt_id,
        string_agg(
            lower(strftime(('2000-01-01 ' || value)::timestamp, '%I:%M %p')),
            ', '
            order by _dlt_list_idx
        )                               as refresh_times_list
    from {{ source('raw_pbi_admin', 'scanner_workspaces__datasets__refresh_schedule__times') }}
    group by _dlt_parent_id
)
{% else %}
refresh_times as (
    select null::varchar as dataset_dlt_id, null::varchar as refresh_times_list
    where 1 = 0
)
{% endif %}

select
    -- Workspace context
    w.workspace_id,
    w.workspace_name,

    -- Semantic model
    d.dataset_id,
    d.dataset_name,
    d.configured_by,
    d.target_storage_mode,
    d.created_at                                            as dataset_created_at,

    -- Refresh schedule
    coalesce(rt.refresh_times_list, 'No schedule')         as refresh_schedule,
    coalesce(d.refresh_schedule_timezone, 'No schedule')   as refresh_timezone,

    -- Datasource details
    di.datasource_id,
    di.datasource_type,
    di.server,
    di.database,
    di.file_path,
    di.url,
    di.gateway_id

from datasets d
inner join workspaces w
    on d.workspace_dlt_id = w._dlt_id
inner join datasource_usages du
    on du.dataset_dlt_id = d._dlt_id
inner join datasource_instances di
    on di.datasource_id = du.datasource_instance_id
left join refresh_times rt
    on rt.dataset_dlt_id = d._dlt_id
