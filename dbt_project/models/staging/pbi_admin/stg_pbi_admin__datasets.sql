-- stg_pbi_admin__datasets.sql
-- Source: Power BI Admin API — GET /admin/datasets
-- One row per dataset (semantic model) across all workspaces in the tenant.
-- Note: dlt normalises all column names to snake_case.

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'datasets'
) %}

{% if relation %}

select
    id                                  as dataset_id,
    name                                as dataset_name,
    configured_by,
    workspace_id,
    is_refreshable,
    is_in_place_sharing_enabled,
    target_storage_mode,
    content_provider_type,
    try_cast(created_date as timestamp) as created_at,
    web_url,
    description,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'datasets') }}

{% else %}

select
    null::varchar   as dataset_id,
    null::varchar   as dataset_name,
    null::varchar   as configured_by,
    null::varchar   as workspace_id,
    null::boolean   as is_refreshable,
    null::boolean   as is_in_place_sharing_enabled,
    null::varchar   as target_storage_mode,
    null::varchar   as content_provider_type,
    null::timestamp as created_at,
    null::varchar   as web_url,
    null::varchar   as description,
    null::varchar   as _dlt_load_id,
    null::varchar   as _dlt_id
where 1 = 0

{% endif %}
