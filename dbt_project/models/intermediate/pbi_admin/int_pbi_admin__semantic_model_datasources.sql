-- int_pbi_admin__semantic_model_datasources.sql
-- Semantic models joined to their data sources.
-- One row per (semantic model, datasource) pair.
-- A model using 2 Excel files + 1 Dataverse connection produces 3 rows.

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
)

select
    -- Workspace context
    w.workspace_id,
    w.workspace_name,

    -- Semantic model
    d.dataset_id,
    d.dataset_name,
    d.configured_by,
    d.target_storage_mode,
    d.created_at                    as dataset_created_at,

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
