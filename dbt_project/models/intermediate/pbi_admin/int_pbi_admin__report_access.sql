-- int_pbi_admin__report_access.sql
-- Per-user access rights to Power BI reports.
-- One row per (report, user) pair across all scanned workspaces.

with report_users as (
    select * from {{ ref('stg_pbi_admin__scanner_report_users') }}
),

reports as (
    select * from {{ ref('stg_pbi_admin__scanner_reports') }}
),

workspaces as (
    select * from {{ ref('stg_pbi_admin__scanner_workspaces') }}
)

select
    -- Workspace context
    w.workspace_id,
    w.workspace_name,

    -- Report context
    r.report_id,
    r.report_name,
    r.report_type,
    r.dataset_id,

    -- User access
    ru.display_name,
    ru.email_address,
    ru.identifier,
    ru.principal_type,
    ru.access_right,
    ru.user_type,
    ru.graph_id

from report_users ru
inner join reports r
    on ru.report_dlt_id = r._dlt_id
inner join workspaces w
    on r.workspace_dlt_id = w._dlt_id
