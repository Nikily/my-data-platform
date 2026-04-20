-- stg_pbi_admin__scanner_datasets__datasource_usages.sql
-- Source: dlt child table scanner_workspaces__datasets__datasource_usages
-- Bridge table: links each dataset to one or more datasource instances.
-- One row per (dataset, datasource_instance) pair.
-- Join to stg_pbi_admin__scanner_datasets on _dlt_parent_id = _dlt_id,
-- then to stg_pbi_admin__scanner_datasource_instances on datasource_instance_id = datasource_id.

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'scanner_workspaces__datasets__datasource_usages'
) %}

{% if relation %}

select
    _dlt_parent_id          as dataset_dlt_id,
    datasource_instance_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'scanner_workspaces__datasets__datasource_usages') }}

{% else %}

select
    null::varchar   as dataset_dlt_id,
    null::varchar   as datasource_instance_id,
    null::varchar   as _dlt_id
where 1 = 0

{% endif %}
