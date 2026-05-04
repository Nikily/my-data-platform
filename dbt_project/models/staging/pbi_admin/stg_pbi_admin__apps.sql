-- stg_pbi_admin__apps.sql
-- Source: Power BI Admin API — GET /admin/apps
-- One row per Power BI app published in the tenant.
-- Note: dlt normalises all column names to snake_case.

{% set relation = adapter.get_relation(
    database   = 'platform',
    schema     = 'raw_pbi_admin',
    identifier = 'apps'
) %}

{% if relation %}

select
    id                                      as app_id,
    name                                    as app_name,
    description                             as app_description,
    published_by,
    try_cast(last_update as timestamp)      as last_updated_at,
    workspace_id,

    _dlt_load_id,
    _dlt_id

from {{ source('raw_pbi_admin', 'apps') }}

{% else %}

select
    null::varchar   as app_id,
    null::varchar   as app_name,
    null::varchar   as app_description,
    null::varchar   as published_by,
    null::timestamp as last_updated_at,
    null::varchar   as workspace_id,
    null::varchar   as _dlt_load_id,
    null::varchar   as _dlt_id
where 1 = 0

{% endif %}
