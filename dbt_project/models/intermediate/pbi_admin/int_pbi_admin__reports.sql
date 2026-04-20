-- int_pbi_admin__reports.sql
-- All Power BI reports enriched with workspace name and semantic model name.
-- One row per report across all scanned workspaces.

with reports as (
    select * from {{ ref('stg_pbi_admin__scanner_reports') }}
),

workspaces as (
    select * from {{ ref('stg_pbi_admin__scanner_workspaces') }}
),

datasets as (
    select * from {{ ref('stg_pbi_admin__scanner_datasets') }}
)

select
    -- Workspace context
    w.workspace_id,
    w.workspace_name,
    w.workspace_type,
    w.workspace_state,

    -- Report fields
    r.report_id,
    r.report_name,
    r.report_type,
    r.app_id,
    r.description,
    r.created_at,
    r.modified_at,
    r.modified_by,

    -- Linked semantic model
    r.dataset_id,
    d.dataset_name,
    r.dataset_workspace_id,

    -- dlt metadata
    r._dlt_load_id,
    r._dlt_id

from reports r
inner join workspaces w
    on r.workspace_dlt_id = w._dlt_id
left join datasets d
    on r.dataset_id = d.dataset_id
