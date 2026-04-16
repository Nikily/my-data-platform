-- stg_pbi_admin__scanner_workspace_users.sql
-- Source: dlt child table scanner_workspaces__users
-- One row per (workspace, user) access entry.
-- Join to stg_pbi_admin__scanner_workspaces on _dlt_parent_id = _dlt_id.

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'scanner_workspaces__users'
) %}

{% if relation %}

select
    _dlt_parent_id                  as workspace_dlt_id,
    display_name,
    email_address,
    identifier,
    graph_id,
    principal_type,
    group_user_access_right         as access_right,
    user_type,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'scanner_workspaces__users') }}

{% else %}

select
    null::varchar   as workspace_dlt_id,
    null::varchar   as display_name,
    null::varchar   as email_address,
    null::varchar   as identifier,
    null::varchar   as graph_id,
    null::varchar   as principal_type,
    null::varchar   as access_right,
    null::varchar   as user_type,
    null::varchar   as _dlt_load_id,
    null::varchar   as _dlt_id
where 1 = 0

{% endif %}
