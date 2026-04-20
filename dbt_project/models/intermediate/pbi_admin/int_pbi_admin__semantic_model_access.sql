-- int_pbi_admin__semantic_model_access.sql
-- Per-user access rights to Power BI semantic models (datasets).
-- One row per (dataset, user) pair across all scanned workspaces.

with dataset_users as (
    select * from {{ ref('stg_pbi_admin__scanner_dataset_users') }}
),

datasets as (
    select * from {{ ref('stg_pbi_admin__scanner_datasets') }}
),

workspaces as (
    select * from {{ ref('stg_pbi_admin__scanner_workspaces') }}
)

select
    -- Workspace context
    w.workspace_id,
    w.workspace_name,

    -- Semantic model context
    d.dataset_id,
    d.dataset_name,
    d.configured_by,

    -- User access
    du.display_name,
    du.email_address,
    du.identifier,
    du.principal_type,
    du.access_right,
    du.user_type,
    du.graph_id

from dataset_users du
inner join datasets d
    on du.dataset_dlt_id = d._dlt_id
inner join workspaces w
    on d.workspace_dlt_id = w._dlt_id
